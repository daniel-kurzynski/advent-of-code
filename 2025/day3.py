from aocd import get_data, submit
import numpy as np

# data = "987654321111111\n811111111111119\n234234234234278\n818181911112111"
data = get_data(day=3, year=2025)

def solve(num_digits=2):
    lines = [[int(c) for c in line] for line in data.strip().split('\n')]
    total = 0

    for line in lines:
        number = 0
        pos = 0

        for i in range(num_digits):
            sublist = line[pos:len(line) - (num_digits - i - 1)]
            digit = max(sublist)
            number = number * 10 + digit
            pos += sublist.index(digit) + 1

        total += number

    return total

print('Part 1:', solve(2))
print('Part 2:', solve(12))