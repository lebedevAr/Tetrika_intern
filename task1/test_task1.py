import unittest
from solution import sum_two


class TestStrictDecorator(unittest.TestCase):
    def test_correct_args(self):
        self.assertEqual(sum_two(1, 2), 3)

    def test_incorrect_first_arg(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1.5, 2)
        self.assertEqual(
            str(context.exception),
            "Argument 'a' must be <class 'int'>, not <class 'float'>"
        )

    def test_incorrect_second_arg(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1, 2.4)
        self.assertEqual(
            str(context.exception),
            "Argument 'b' must be <class 'int'>, not <class 'float'>"
        )

    def test_correct_kwargs(self):
        self.assertEqual(sum_two(a=1, b=2), 3)

    def test_incorrect_kwarg(self):
        with self.assertRaises(TypeError) as context:
            sum_two(a=1, b=2.4)
        self.assertEqual(
            str(context.exception),
            "Argument 'b' must be <class 'int'>, not <class 'float'>"
        )

    def test_mixed_args_kwargs(self):
        self.assertEqual(sum_two(1, b=2), 3)

    def test_incorrect_mixed_args_kwargs(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1.5, b=2)
        self.assertEqual(
            str(context.exception),
            "Argument 'a' must be <class 'int'>, not <class 'float'>"
        )


if __name__ == "__main__":
    unittest.main()