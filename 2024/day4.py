from aocd import get_data, submit
import numpy as np

data = "MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX"
# data = get_data(day=4, year=2024)

def parse(input):
    lines = input.split('\n')
    return np.array([list(line) for line in lines])

def count_xmas(text):
    return text.count('XMAS') + text[::-1].count('XMAS')

def part1(input):
    grid = parse(input)
    count = 0

    for line in grid:
        count += count_xmas(''.join(line))
    for line in grid.T:
        count += count_xmas(''.join(line))

    rows, cols = grid.shape
    for offset in range(-rows + 1, cols):
        for g in [grid, np.fliplr(grid)]:
            count += count_xmas(''.join(g.diagonal(offset)))

    return count

def part2(input):
    grid = parse(input)
    rows, cols = grid.shape
    count = 0

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if grid[i, j] == 'A':
                if ["M", "S"]  == sorted([grid[i-1, j-1], grid[i+1, j+1]]) == sorted([grid[i-1, j+1], grid[i+1, j-1]]):
                    count += 1

    return count

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")