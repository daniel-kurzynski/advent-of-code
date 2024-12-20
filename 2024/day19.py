from aocd import get_data, submit
from functools import cache

data = "r, wr, b, g, bwu, rb, gb, br\n\nbrwrr\nbggr\ngbbr\nrrbgbr\nubwu\nbwurrg\nbrgr\nbbrgwb"  # Example data
data = get_data(day=19, year=2024)

def parse_data(input):
    towels, designs = input.split('\n\n')
    available_towels = {t.strip() for t in towels.split(',')}
    desired_designs = designs.split('\n')
    max_towel_length = max(len(towel) for towel in available_towels)
    return available_towels, desired_designs, max_towel_length

@cache
def is_possible(design, towels_frozen, max_length):
    if not design:
        return 1

    ways = 0
    for length in range(1, min(len(design) + 1, max_length + 1)):
        prefix = design[:length]
        if prefix in towels_frozen:
            ways += is_possible(design[length:], towels_frozen, max_length)

    return ways

def solve(input):
    towels, designs, max_length = parse_data(input)
    towels_frozen = frozenset(towels)  # Make towels hashable for caching
    possible_ways = [is_possible(design, towels_frozen, max_length) for design in designs]
    return possible_ways

def part1(possible_ways):
    return sum(1 for ways in possible_ways if ways > 0)

def part2(possible_ways):
    return sum(possible_ways)

possible_ways = solve(data)
print(f"Part 1: {part1(possible_ways)}")
print(f"Part 2: {part2(possible_ways)}")