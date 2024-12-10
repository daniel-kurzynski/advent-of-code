from aocd import get_data, submit
import numpy as np
from collections import deque

# data = "89010123\n78121874\n87430965\n96549874\n45678903\n32019012\n01329801\n10456732"  # Example data
data = get_data(day=10, year=2024)

def parse_data(input):
    return np.array([[int(x) for x in line] for line in input.splitlines()])

def search_trails(grid, start_r, start_c, count_all_paths=False):
    rows, cols = grid.shape
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    if count_all_paths:
        def dfs(r, c):
            current_height = grid[r, c]
            if current_height == 9:
                return 1

            total_paths = 0
            for dr, dc in directions:
                new_r, new_c = r + dr, c + dc
                if (0 <= new_r < rows and
                        0 <= new_c < cols and
                        grid[new_r, new_c] == current_height + 1):
                    total_paths += dfs(new_r, new_c)
            return total_paths

        return dfs(start_r, start_c)
    else:
        queue = deque([(start_r, start_c)])
        reachable_nines = set()

        while queue:
            r, c = queue.popleft()
            current_height = grid[r, c]

            if current_height == 9:
                reachable_nines.add((r, c))
                continue

            for dr, dc in directions:
                new_r, new_c = r + dr, c + dc
                if (0 <= new_r < rows and
                        0 <= new_c < cols and
                        grid[new_r, new_c] == current_height + 1):
                    queue.append((new_r, new_c))

        return len(reachable_nines)

def solve(grid, count_all_paths=False):
    total = 0

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 0:
                total += search_trails(grid, r, c, count_all_paths)

    return total

grid = parse_data(data)

def part1(input):
    return solve(grid, False)

def part2(input):
    return solve(grid, True)

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")