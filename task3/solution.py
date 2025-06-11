def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    def process_intervals(timestamps):
        intervals = []
        for i in range(0, len(timestamps), 2):
            start = timestamps[i]
            end = timestamps[i + 1]
            intervals.append((start, end))
        intervals.sort()
        merged = []
        for interval in intervals:
            if not merged:
                merged.append(interval)
            else:
                last_start, last_end = merged[-1]
                current_start, current_end = interval
                if current_start <= last_end:
                    new_start = last_start
                    new_end = max(last_end, current_end)
                    merged[-1] = (new_start, new_end)
                else:
                    merged.append(interval)
        return merged

    pupil_merged = process_intervals(pupil)
    tutor_merged = process_intervals(tutor)
    lesson_start, lesson_end = lesson

    def intersect_with_lesson(intervals):
        result = []
        for start, end in intervals:
            current_start = max(start, lesson_start)
            current_end = min(end, lesson_end)
            if current_start < current_end:
                result.append((current_start, current_end))
        return result

    pupil_in_lesson = intersect_with_lesson(pupil_merged)
    tutor_in_lesson = intersect_with_lesson(tutor_merged)

    def find_common_time(pupil, tutor):
        i = j = 0
        common_time = 0
        while i < len(pupil) and j < len(tutor):
            pupil_start, pupil_end = pupil[i]
            tutor_start, tutor_end = tutor[j]

            overlap_start = max(pupil_start, tutor_start)
            overlap_end = min(pupil_end, tutor_end)

            if overlap_start < overlap_end:
                common_time += overlap_end - overlap_start

            if pupil_end < tutor_end:
                i += 1
            else:
                j += 1
        return common_time

    return find_common_time(pupil_in_lesson, tutor_in_lesson)

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

