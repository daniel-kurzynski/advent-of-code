from aocd import get_data, submit
import numpy as np
from collections import deque

data, size, bytes = "5,4\n4,2\n4,5\n3,0\n2,1\n6,3\n2,4\n1,5\n0,6\n3,3\n2,6\n5,1\n1,2\n5,5\n2,5\n6,5\n1,4\n0,4\n6,4\n1,1\n6,1\n1,0\n0,5\n1,6\n2,0", 6, 12  # Example data
data, size, bytes = get_data(day=18, year=2024), 70, 1024

def parse_data(input):
    return [tuple(map(int, line.split(','))) for line in input.splitlines()]

def bfs(grid):
    grid_size = len(grid) - 1
    queue = deque([(0, 0, 0)])
    visited = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == (grid_size, grid_size):
            return steps

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x <= grid_size and
                    0 <= new_y <= grid_size and
                    grid[new_y, new_x] == 0):  # not corrupted
                queue.append((new_x, new_y, steps + 1))

    return None  # No path found

def solve(input, grid_size, byte_limit):
    coords = parse_data(input)
    grid = np.zeros((grid_size + 1, grid_size + 1), dtype=int)

    for x, y in coords[:byte_limit]:
        grid[y, x] = 1

    return bfs(grid)

def part1(input, grid_size, byte_limit):
    return solve(input, grid_size, byte_limit)

def part2(input, grid_size, byte_limit):
    coords = parse_data(input)
    maximum_working = 0
    minimum_not_working = (grid_size + 1) ** 2

    while maximum_working + 1 < minimum_not_working:
        mid = (maximum_working + minimum_not_working) // 2
        path = solve(input, grid_size, mid)

        if path is not None:
            maximum_working = mid
        else:
            minimum_not_working = mid

    # Return the coordinates that first blocked the path
    return f"{coords[minimum_not_working-1][0]},{coords[minimum_not_working-1][1]}"

print(f"Part 1: {part1(data, size, bytes)}")
print(f"Part 2: {part2(data, size, bytes)}")