from aocd import get_data, submit
from collections import defaultdict

data = "RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE"
data = "OOO\nORO\nROO"
data = get_data(day=12, year=2024)

def parse_map(input):
    return [list(line) for line in input.split('\n')]

def find_region(grid, x, y, visited, store_fences=False):
    if (x, y) in visited:
        return 0, 0, set()

    rows, cols = len(grid), len(grid[0])
    plant_type = grid[x][y]
    area = 0
    perimeter = 0
    vertical_fences = defaultdict(set)
    horizontal_fences = defaultdict(set)
    stack = [(x, y)]

    while stack:
        curr_x, curr_y = stack.pop()
        if (curr_x, curr_y) in visited:
            continue

        visited.add((curr_x, curr_y))
        area += 1

        # Check all 4 directions
        for direction, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            next_x, next_y = curr_x + dx, curr_y + dy

            if (next_x < 0 or next_x >= rows or
                    next_y < 0 or next_y >= cols or
                    grid[next_x][next_y] != plant_type):
                perimeter += 1
                if store_fences:
                    if direction % 2 == 0:
                        if (curr_y, next_y) in horizontal_fences:
                            horizontal_fences[curr_y, next_y].add(curr_x)
                        else:
                            horizontal_fences[curr_y, next_y] = {curr_x}
                    else:
                        if (curr_x, next_x) in vertical_fences:
                            vertical_fences[curr_x, next_x].add(curr_y)
                        else:
                            vertical_fences[curr_x, next_x] = {curr_y}
            elif (next_x, next_y) not in visited:
                stack.append((next_x, next_y))

    return area, perimeter, horizontal_fences, vertical_fences

def count_gaps_in_sequence(sequence):
    if not sequence:
        return 0
    sorted_seq = sorted(sequence)
    gaps = sum(1 for i in range(1, len(sorted_seq)) if sorted_seq[i] > sorted_seq[i-1] + 1)
    return gaps + 1

def count_unique_sides(horizontal_fences, vertical_fences):
    sum = 0
    for fences in [horizontal_fences, vertical_fences]:
        for positions in fences.values():
            sum += count_gaps_in_sequence(positions)

    return sum


def part1(input):
    grid = parse_map(input)
    visited = set()
    total_price = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in visited:
                area, perimeter, _, _ = find_region(grid, i, j, visited)
                price = area * perimeter
                total_price += price

    return total_price

def part2(input):
    grid = parse_map(input)
    visited = set()
    total_price = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in visited:
                area, _, horizontal_fences, vertical_fences = find_region(grid, i, j, visited, True)
                sides = count_unique_sides(horizontal_fences, vertical_fences)
                price = area * sides
                total_price += price

    return total_price

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")