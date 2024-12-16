from aocd import get_data, submit
import numpy as np

data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

data = get_data(day=15, year=2024)

def parse_input(data):
    grid_str, moves = data.strip().split('\n\n')
    grid = np.array([list(line) for line in grid_str.splitlines()])

    robot_pos = np.where(grid == '@')
    robot_pos = (robot_pos[0][0], robot_pos[1][0])
    grid[robot_pos] = '.'

    return grid, moves, robot_pos

def widen_grid(grid):
    rows, cols = grid.shape
    wide_grid = np.empty((rows, cols * 2), dtype=str)

    for i in range(rows):
        for j in range(cols):
            if grid[i,j] == '#':
                wide_grid[i,j*2:j*2+2] = ['#', '#']
            elif grid[i,j] == 'O':
                wide_grid[i,j*2:j*2+2] = ['[', ']']
            elif grid[i,j] == '.':
                wide_grid[i,j*2:j*2+2] = ['.', '.']
            elif grid[i,j] == '@':
                wide_grid[i,j*2:j*2+2] = ['@', '.']

    return wide_grid

def find_moves_chain(grid, robot_pos, direction):
    moves = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    dx, dy = moves[direction]
    rows, cols = grid.shape

    new_robot_pos = (robot_pos[0] + dx, robot_pos[1] + dy)
    current_positions = [new_robot_pos]
    moves_list = []

    while True:
        for current_position in current_positions:
            if not (0 <= current_position[0] < rows and 0 <= current_position[1] < cols):
                return None
            if grid[current_position] == '#':
                return None

        if all(grid[current_position] == '.' for current_position in current_positions):
            return moves_list, new_robot_pos

        next_positions = []
        for current_position in current_positions:
            if grid[current_position] == 'O':
                next_position = (current_position[0] + dx, current_position[1] + dy)
                next_positions.append(next_position)
                moves_list.append((current_position, next_position))

            if direction in ['<', '>'] and grid[current_position] in ['[', ']']:
                next_position = (current_position[0], current_position[1] + dy)
                next_next_position = (next_position[0], next_position[1] + dy)
                moves_list.append((current_position, next_position))
                moves_list.append((next_position, next_next_position))
                next_positions.append(next_next_position)

            if direction in ['^', 'v'] and grid[current_position] == '[':
                current_position_left = (current_position[0], current_position[1])
                current_position_right = (current_position[0], current_position[1] + 1)

                next_position_left = (current_position_left[0] + dx, current_position_left[1])
                next_position_right = (current_position_right[0] + dx, current_position_right[1])

                next_positions.append(next_position_left)
                next_positions.append(next_position_right)

                moves_list.append((current_position_left, next_position_left))
                moves_list.append((current_position_right, next_position_right))

            if direction in ['^', 'v'] and grid[current_position] == ']':
                current_position_left = (current_position[0], current_position[1] - 1)
                current_position_right = (current_position[0], current_position[1])

                next_position_left = (current_position_left[0] + dx, current_position_left[1])
                next_position_right = (current_position_right[0] + dx, current_position_right[1])

                next_positions.append(next_position_left)
                next_positions.append(next_position_right)

                moves_list.append((current_position_left, next_position_left))
                moves_list.append((current_position_right, next_position_right))

        current_positions = next_positions

    return None  # Reached edge of grid without finding empty space

def make_move(grid, robot_pos, direction):
    move_result = find_moves_chain(grid, robot_pos, direction)
    if not move_result:
        return grid, robot_pos

    moves_chain, new_robot_pos = move_result

    new_grid = grid.copy()

    # Apply all moves in reverse order to avoid overwriting positions
    for from_pos, to_pos in reversed(moves_chain):
        new_grid[to_pos] = grid[from_pos]
        new_grid[from_pos] = '.'

    return new_grid, new_robot_pos

def calculate_gps_sum(grid, wide=False):
    if wide:
        box_positions = np.where(grid == '[')
        return np.sum(box_positions[0] * 100 + box_positions[1])
    else:
        box_positions = np.where(grid == 'O')
        return np.sum(box_positions[0] * 100 + box_positions[1])

def part1(input):
    grid, moves, robot_pos = parse_input(input)

    for move in moves.strip():
        if move in '^v<>':
            grid, robot_pos = make_move(grid, robot_pos, move)

    return calculate_gps_sum(grid)

def part2(input):
    grid, moves, robot_pos = parse_input(input)
    grid = widen_grid(grid)
    robot_pos = (robot_pos[0], robot_pos[1] * 2)

    for index, move in enumerate(moves.strip()):
        if move in '^v<>':
            grid, robot_pos = make_move(grid, robot_pos, move)

    return calculate_gps_sum(grid, wide=True)

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")