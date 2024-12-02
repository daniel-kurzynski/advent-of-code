from aocd import get_data, submit
import numpy as np

# data = "7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9"  # Example data from puzzle
data = get_data(day=2, year=2024)

def parse(input):
    return [np.array(list(map(int, line.split()))) for line in input.split('\n')]

def unsafe_levels(row):
    diffs = np.diff(row)
    magnitude_check = (np.abs(diffs) >= 1) & (np.abs(diffs) <= 3)

    increasing_check_mask = ~((diffs > 0) & magnitude_check)
    decreasing_check_mask = ~((diffs < 0) & magnitude_check)

    if np.sum(increasing_check_mask) <= np.sum(decreasing_check_mask):
        violations = increasing_check_mask
    else:
        violations = decreasing_check_mask

    violation_indices = np.where(violations)[0]
    return violation_indices

def is_safe_with_dampener(row):
    bad_indices = unsafe_levels(row)
    if len(bad_indices) == 0:
        return True

    for bad_index in bad_indices:
        for idx in range(bad_index - 1, bad_index + 2):
            new_row = np.delete(row, idx)
            if len(unsafe_levels(new_row)) == 0:
                return True
    return False

def part1(data):
    return sum(1 for row in data if len(unsafe_levels(row)) == 0)

def part2(data):
    return sum(1 for row in data if is_safe_with_dampener(row))

parsed_data = parse(data)
print(f"Part 1: {part1(parsed_data)}")
print(f"Part 2: {part2(parsed_data)}")