import unittest
from unittest.mock import patch, MagicMock
import csv
import tempfile
import os
from solution import process_page, get_animals_count, save_to_csv, letter_counts


class TestWikiAnimalsCount(unittest.TestCase):
    def setUp(self):
        # Сброс глобального счетчика перед каждым тестом
        global letter_counts
        letter_counts.clear()

    @patch('requests.get')
    def test_process_page_success(self, mock_get):
        """Тест обработки одной страницы с валидными данными."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'query': {
                'categorymembers': [
                    {'title': 'Аист'},
                    {'title': 'Баран'},
                    {'title': 'Бобр'},
                    {'title': 'Ягуар'},
                    {'title': '123Неживотное'},  # Должно игнорироваться
                    {'title': 'Zebra'},  # Должно игнорироваться (не кириллица)
                ]
            },
            'continue': {'cmcontinue': 'next_page'}
        }
        mock_get.return_value = mock_response

        result = process_page("https://ru.wikipedia.org/w/api.php", {})

        self.assertEqual(result, {'cmcontinue': 'next_page'})
        self.assertEqual(letter_counts, {'А': 1, 'Б': 2, 'Я': 1})

    @patch('requests.get')
    def test_process_page_no_query(self, mock_get):
        """Тест обработки страницы без данных."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = process_page("https://ru.wikipedia.org/w/api.php", {})

        self.assertIsNone(result)
        self.assertEqual(letter_counts, {})

    @patch('solution.process_page')
    @patch('solution.ThreadPoolExecutor')
    def test_get_animals_count(self, mock_executor, mock_process):
        """Тест основной функции сбора данных."""
        # Настраиваем mock для ThreadPoolExecutor
        mock_future = MagicMock()
        mock_future.result.side_effect = [
            {'cmcontinue': 'page2'},  # Первый вызов
            {'cmcontinue': 'page3'},   # Второй вызов
            None                      # Третий вызов (конец)
        ]
        mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future

        counts = get_animals_count()

        # Проверяем, что submit вызывался 3 раза
        self.assertEqual(mock_executor.return_value.__enter__.return_value.submit.call_count, 3)
        # Проверяем, что результат - отсортированный словарь (даже если пустой)
        self.assertIsInstance(counts, dict)

    def test_save_to_csv(self):
        """Тест сохранения данных в CSV."""
        test_data = {'А': 10, 'Б': 5, 'В': 3}

        # Используем временный файл
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmpfile:
            tmpfile.close()
            try:
                save_to_csv(test_data, tmpfile.name)

                # Проверяем содержимое файла
                with open(tmpfile.name, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    rows = list(reader)

                self.assertEqual(rows, [['А', '10'], ['Б', '5'], ['В', '3']])
            finally:
                os.unlink(tmpfile.name)


if __name__ == '__main__':
    unittest.main()