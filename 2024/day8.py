from aocd import get_data, submit
import numpy as np
from collections import defaultdict

# data = "............\n........0...\n.....0......\n.......0....\n....0.......\n......A.....\n............\n............\n........A...\n.........A..\n............\n............"  # Example data
data = get_data(day=8, year=2024)

def parse_data(input):
    lines = input.split('\n')
    grid = np.array([list(line) for line in lines])

    antennas = defaultdict(list)

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y,x] != '.':
                antennas[grid[y,x]].append((x, y))

    return antennas, (grid.shape[1], grid.shape[0])

def calculate_antinodes(antennas, size, use_multiples=False):
    width, height = size
    antinodes = set()

    for signal, coords in antennas.items():
        if len(coords) > 1:
            if use_multiples:
                for coord in coords:
                    antinodes.add(coord)

            for i in range(len(coords)):
                for j in range(i + 1, len(coords)):
                    x1, y1 = coords[i]
                    x2, y2 = coords[j]

                    dx = x2 - x1
                    dy = y2 - y1

                    mult = 1
                    while True:
                        x_node = x1 - dx * mult
                        y_node = y1 - dy * mult
                        if 0 <= x_node < width and 0 <= y_node < height:
                            antinodes.add((x_node, y_node))
                        else:
                            break
                        if not use_multiples and mult >= 1:
                            break
                        mult += 1

                    mult = 1
                    while True:
                        x_node = x2 + dx * mult
                        y_node = y2 + dy * mult
                        if 0 <= x_node < width and 0 <= y_node < height:
                            antinodes.add((x_node, y_node))
                        else:
                            break
                        if not use_multiples and mult >= 1:
                            break
                        mult += 1

    return len(antinodes)

def part1(antennas, size):
    return calculate_antinodes(antennas, size, False)

def part2(antennas, size):
    return calculate_antinodes(antennas, size, True)

antennas, size = parse_data(data)

print(f"Part 1: {part1(antennas, size)}")
print(f"Part 2: {part2(antennas, size)}")