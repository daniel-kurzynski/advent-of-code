from aocd import get_data, submit
import numpy as np

# data = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3"
data = get_data(day=1, year=2024)

def parse_input(input):
    return np.array([list(map(int, line.split())) for line in input.split('\n')])

def part1(numbers):
    sorted_cols = np.sort(numbers, axis=0)
    differences = np.abs(sorted_cols[:, 0] - sorted_cols[:, 1])
    return np.sum(differences)

def part2(numbers):
    left_list = numbers[:, 0]
    right_list = numbers[:, 1]

    similarity_score = sum(num * np.count_nonzero(right_list == num) for num in left_list)
    return similarity_score

parsed_data = parse_input(data)
print(f"Part 1: {part1(parsed_data)}")
print(f"Part 2: {part2(parsed_data)}")