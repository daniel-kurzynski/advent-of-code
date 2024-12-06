from aocd import get_data, submit
import numpy as np

# data = "....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#..."
data = get_data(day=6, year=2024)

def parse_input(input):
    lines = input.splitlines()
    height = len(lines)
    width = len(lines[0])
    grid = np.zeros((height, width), dtype=bool)
    start_pos = None

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                grid[i, j] = True
            elif char == '^':
                start_pos = (i, j)

    return start_pos, grid

def find_loop_or_exit(start_pos, grid):
    direction = (-1, 0)
    current_pos = start_pos
    visited = {(current_pos, direction)}
    height, width = grid.shape

    while True:
        next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])

        if (next_pos[0] < 0 or next_pos[0] >= height or
                next_pos[1] < 0 or next_pos[1] >= width):
            return False, visited

        if grid[next_pos]:
            direction = (direction[1], -direction[0])
        else:
            current_pos = next_pos
            state = (current_pos, direction)
            if state in visited:
                return True, visited
            visited.add(state)

    raise ValueError("Should not reach here")

def part1(start_pos, grid):
    loop, visited = find_loop_or_exit(start_pos, grid)
    return len({coordinate for coordinate, _ in visited})

def part2(start_pos, grid):
    direction = (-1, 0)
    current_pos = start_pos
    loop_positions = set()
    visited_states = {(current_pos, direction)}
    height, width = grid.shape

    while True:
        next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])

        if (next_pos[0] < 0 or next_pos[0] >= height or
                next_pos[1] < 0 or next_pos[1] >= width):
            break

        if not grid[next_pos]:
            if next_pos != start_pos:

                grid[next_pos] = True
                found_loop, _ = find_loop_or_exit(start_pos, grid)
                if found_loop:
                    loop_positions.add(next_pos)
                grid[next_pos] = False

            current_pos = next_pos
            state = (current_pos, direction)
            if state in visited_states:
                break
            visited_states.add(state)
        else:
            direction = (direction[1], -direction[0])

    return len(loop_positions)

start_pos, grid = parse_input(data)

print(f"Part 1: {part1(start_pos, grid)}")
print(f"Part 2: {part2(start_pos, grid)}")