from aocd import get_data, submit
import re

# data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
data = get_data(day=3, year=2024)

def extract_multiplications(text, filter_by_dos=False):
    result = []
    enabled = True
    mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"

    for m in re.finditer(f"{mul_pattern}|{do_pattern}|{dont_pattern}", text):
        if m.group(0).startswith('mul') and (enabled or not filter_by_dos):
            result.append((int(m.group(1)), int(m.group(2))))
        elif m.group(0) == 'do()':
            enabled = True
        elif m.group(0) == "don't()":
            enabled = False

    return result

def part1(input):
    return sum(x * y for x, y in extract_multiplications(input))

def part2(input):
    return sum(x * y for x, y in extract_multiplications(input, filter_by_dos=True))

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")