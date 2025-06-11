import requests
from collections import defaultdict
import csv
from concurrent.futures import ThreadPoolExecutor
import threading

# Глобальные переменные для многопоточной работы
lock = threading.Lock()
letter_counts = defaultdict(int)


def process_page(base_url, params):
    global letter_counts
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'query' not in data:
        return None

    page_counts = defaultdict(int)
    for member in data['query']['categorymembers']:
        title = member['title']
        first_letter = title[0].upper()
        if 'А' <= first_letter <= 'Я':
            page_counts[first_letter] += 1

    # Безопасное обновление общего счетчика
    with lock:
        for letter, count in page_counts.items():
            letter_counts[letter] += count

    return data.get('continue')


def get_animals_count():
    base_url = "https://ru.wikipedia.org/w/api.php"
    continue_params = {}

    with ThreadPoolExecutor(max_workers=12) as executor:
        while True:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'categorymembers',
                'cmtitle': 'Категория:Животные по алфавиту',
                'cmlimit': '500',
                **continue_params
            }

            future = executor.submit(process_page, base_url, params)
            result = future.result()

            if result:
                continue_params = result
            else:
                break

    return dict(sorted(letter_counts.items()))


def save_to_csv(letter_counts, filename='beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in letter_counts.items():
            writer.writerow([letter, count])


if __name__ == "__main__":
    counts = get_animals_count()
    save_to_csv(counts)
    print("Данные успешно сохранены в beasts.csv")