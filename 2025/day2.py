from aocd import get_data, submit
import math

# data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
data = get_data(day=2, year=2025)

def preprocess(raw: str):
    return [(int(start), int(end)) for part in raw.split(',') if part.strip() for start, end in [part.strip().split('-')]]

def num_digits(n):
    if n == 0:
        return 1
    return int(math.log10(abs(n))) + 1

def repeat_number(n, times):
    """Repeat a number 'times' times. E.g., repeat_number(12, 3) = 121212"""
    n_digits = num_digits(n)
    result = 0
    for i in range(times):
        result = result * (10 ** n_digits) + n
    return result

def first_n_digits(num, n):
    """Get the first n digits of a number"""
    digits = num_digits(num)
    if n >= digits:
        return num
    return num // (10 ** (digits - n))

def find_invalid_ids(range_tuple, multi_repeats=False):
    start, end = range_tuple
    invalid_ids = set()

    max_length = num_digits(end)
    min_length = num_digits(start)

    if multi_repeats:
        pattern_length_start = 1
    else:
        pattern_length_start = max(1, num_digits(start) // 2)

    for pattern_length in range(pattern_length_start, max_length // 2 + 1):
        if multi_repeats:
            has_multiple_in_range = False
            for num_repeats in range(2, (max_length // pattern_length) + 2):
                multiple_length = pattern_length * num_repeats
                if min_length <= multiple_length <= max_length:
                    has_multiple_in_range = True
                    break

            if not has_multiple_in_range:
                continue

        starting_pattern = 1 if pattern_length == 1 else 10 ** (pattern_length - 1)
        current_pattern = starting_pattern

        while True:
            if num_digits(current_pattern) == pattern_length:
                if multi_repeats:
                    repeat_range = range(2, (max_length // pattern_length) + 2)
                else:
                    repeat_range = [2]  # Only exactly 2 repeats for Part 1

                for num_repeats in repeat_range:
                    id_to_check = repeat_number(current_pattern, num_repeats)

                    if num_repeats == 2 and id_to_check > end:
                        break

                    if id_to_check > end:
                        break

                    if id_to_check >= start:
                        invalid_ids.add(id_to_check)

            current_pattern += 1

            if num_digits(current_pattern) == pattern_length:
                smallest_multiple = repeat_number(current_pattern, 2)
                if smallest_multiple > end:
                    break
            elif num_digits(current_pattern) > pattern_length:
                break

    return invalid_ids

range_tuples = preprocess(data)

print('Part 1:', sum(sum(find_invalid_ids(range_tuple, False)) for range_tuple in range_tuples))
print('Part 2:', sum(sum(find_invalid_ids(range_tuple, True)) for range_tuple in range_tuples))