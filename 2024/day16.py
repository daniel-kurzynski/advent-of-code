from aocd import get_data, submit
import numpy as np
from queue import PriorityQueue

data = "###############\n#.......#....E#\n#.#.###.#.###.#\n#.....#.#...#.#\n#.###.#####.#.#\n#.#.#.......#.#\n#.#.#####.###.#\n#...........#.#\n###.#.#####.#.#\n#...#.....#.#.#\n#.#.#.###.#.#.#\n#.....#...#.#.#\n#.###.#.#.#.#.#\n#S..#.....#...#\n###############"  # Example data
data = get_data(day=16, year=2024)

def parse_input(input):
    grid = np.array([list(line) for line in input.splitlines()])
    start_pos = tuple(np.argwhere(grid == 'S')[0])
    return grid, start_pos


def solve(input):
    grid, start_pos = parse_input(input)
    queue = PriorityQueue()

    # Start facing east (0 = east, 1 = south, 2 = west, 3 = north)
    start_direction = 0
    queue.put((0, (start_pos[0], start_pos[1], start_direction, {start_pos})))
    min_score = float('inf')

    visited = set()

    moves = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}  # east, south, west, north

    while not queue.empty():
        score, (row, col, direction, on_path) = queue.get()

        if (row, col, direction) in visited:
            continue

        visited.add((row, col, direction))

        similar_positions = []
        on_path = on_path.copy()

        while not queue.empty() and queue.queue[0][0] == score:
            next_score, (next_row, next_col, next_dir, next_on_path) = queue.get()
            if (next_row, next_col) == (row, col):
                on_path.update(next_on_path)
            else:
                similar_positions.append((next_score, (next_row, next_col, next_dir, next_on_path)))

        for pos in similar_positions:
            queue.put(pos)

        if grid[row, col] == 'E':
            return score, len(on_path)

        # Handle turns plus movement
        for new_dir in [(direction - 1) % 4, (direction + 1) % 4]:  # left and right turns
            dr, dc = moves[new_dir]
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row, new_col] != '#':
                new_on_path = on_path | {(new_row, new_col)}
                queue.put((score + 1001, (new_row, new_col, new_dir, new_on_path)))  # 1000 for turn + 1 for move

        # Handle forward movement (cost 1)
        dr, dc = moves[direction]
        new_row, new_col = row + dr, col + dc

        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row, new_col] != '#':
            new_on_path = on_path | {(new_row, new_col)}
            queue.put((score + 1, (new_row, new_col, direction, new_on_path)))

    return min_score

score, unique_coords_count = solve(data)
print(f"Part 1: {score}")
print(f"Part 2: {unique_coords_count}")