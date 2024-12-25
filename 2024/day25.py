from aocd import get_data, submit
import numpy as np

data = """#####\n.####\n.####\n.####\n.#.#.\n.#...\n.....\n\n#####\n##.##\n.#.##\n...##\n...#.\n...#.\n.....\n\n.....\n#....\n#....\n#...#\n#.#.#\n#.###\n#####\n\n.....\n.....\n#.#..\n###..\n###.#\n###.#\n#####\n\n.....\n.....\n.....\n#....\n#.#..\n#.#.#\n#####"""  # Example data
data = get_data(day=25, year=2024)

def parse_data(input):
    locks, keys = [], []
    for schematic in input.split('\n\n'):
        grid = np.array([list(line) for line in schematic.splitlines()])
        heights = np.sum(grid == '#', axis=0) - 1
        (locks if grid[0,0] == '#' else keys).append(heights)
    return locks, keys

def part1(input):
    locks, keys = parse_data(input)
    return sum(np.all(l + k <= 5) for l in locks for k in keys)

print(f"Part 1: {part1(data)}")