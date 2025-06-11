import unittest
from solution import appearance


class TestAppearance(unittest.TestCase):
    def test_basic_case(self):
        intervals = {
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
        }
        self.assertEqual(appearance(intervals), 3117)

    def test_complex_case(self):
        intervals = {
            'lesson': [1594702800, 1594706400],
            'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513,
                      1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009,
                      1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773,
                      1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                      1594706524, 1594706524, 1594706579, 1594706641],
            'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
        }
        self.assertEqual(appearance(intervals), 3577)


    def test_full_overlap(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [100, 200],
            'tutor': [100, 200]
        }
        self.assertEqual(appearance(intervals), 100)

    def test_partial_overlap(self):
        intervals = {
            'lesson': [100, 250],
            'pupil': [50, 200],
            'tutor': [150, 250]
        }
        self.assertEqual(appearance(intervals), 50)

    def test_multiple_intervals(self):
        intervals = {
            'lesson': [100, 500],
            'pupil': [100, 150, 200, 250, 300, 350],
            'tutor': [125, 175, 225, 275, 325, 375]
        }
        self.assertEqual(appearance(intervals), 75)

    def test_empty_pupil_or_tutor(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [],
            'tutor': [150, 250]
        }
        self.assertEqual(appearance(intervals), 0)

        intervals = {
            'lesson': [100, 200],
            'pupil': [150, 250],
            'tutor': []
        }
        self.assertEqual(appearance(intervals), 0)

    def test_edge_case_single_point(self):
        intervals = {
            'lesson': [100, 200],
            'pupil': [150, 150],
            'tutor': [150, 150]
        }
        self.assertEqual(appearance(intervals), 0)


if __name__ == '__main__':
    unittest.main()