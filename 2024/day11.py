from aocd import get_data, submit
from functools import cache

def parse_data(input):
    return [int(x) for x in input.split()]

def apply_rules(stone):
    # Rule 1: If stone is 0, becomes 1
    if stone == 0:
        return [1]

    # Rule 2: If even number of digits, split into two stones
    elif len(str(stone)) % 2 == 0:
        digits = str(stone)
        mid = len(digits) // 2
        return [int(digits[:mid]), int(digits[mid:])]

    # Rule 3: Otherwise multiply by 2024
    else:
        return [stone * 2024]

@cache
def solve(stone, blinks):
    if blinks == 0:
        return 1

    new_stones = apply_rules(stone)
    return sum(solve(new_stone, blinks - 1) for new_stone in new_stones)

def part1(input):
    stones = parse_data(input)
    return sum(solve(stone, 25) for stone in stones)

def part2(input):
    stones = parse_data(input)
    return sum(solve(stone, 75) for stone in stones)

data = "125 17"
data = get_data(day=11, year=2024)

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")