from aocd import get_data, submit
import re
from collections import defaultdict

data = "p=0,4 v=3,-3\np=6,3 v=-1,-3\np=10,3 v=-1,2\np=2,0 v=2,-1\np=0,0 v=1,3\np=3,0 v=-2,-2\np=7,6 v=-1,-3\np=3,0 v=-1,-2\np=9,3 v=2,3\np=7,3 v=-1,2\np=2,4 v=2,-3\np=9,5 v=-3,-3"  # Example data
data = get_data(day=14, year=2024)

def parse_input(input):
    pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
    robots = []
    for line in input.split('\n'):
        match = re.match(pattern, line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append(((px, py), (vx, vy)))
    return robots

def calculate_final_positions(robots, time, width, height):
    final_positions = []
    for (px, py), (vx, vy) in robots:
        # Calculate final position using linear algebra
        final_x = (px + vx * time) % width
        final_y = (py + vy * time) % height
        final_positions.append((final_x, final_y))
    return final_positions

def calculate_safety_factor(positions, width, height):
    # Initialize counters for each quadrant
    quadrants = [0, 0, 0, 0]  # [top-left, top-right, bottom-left, bottom-right]
    mid_x = width // 2
    mid_y = height // 2

    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue

        # Determine quadrant
        if x < mid_x:
            if y < mid_y:
                quadrants[0] += 1  # top-left
            else:
                quadrants[2] += 1  # bottom-left
        else:
            if y < mid_y:
                quadrants[1] += 1  # top-right
            else:
                quadrants[3] += 1  # bottom-right

    # Multiply all quadrant counts
    safety_factor = 1
    for count in quadrants:
        safety_factor *= count
    return safety_factor

def check_vertical_line(positions, width, height, total_robots):
    required_robots = total_robots * 0.05

    vertical_lines = defaultdict(set)
    for x, y in positions:
        vertical_lines[x].add(y)

    # Check each vertical line
    for x, y_positions in vertical_lines.items():
        if len(y_positions) >= required_robots:
            y_list = sorted(y_positions)
            for i in range(len(y_list) - 1):
                if (y_list[i + 1] - y_list[i]) % height > 1:  # Gap found
                    break
            else:
                return True, x
    return False, None

def print_grid(positions, width, height):
    grid = [['.'] * width for _ in range(height)]
    position_counts = defaultdict(int)

    # Count robots at each position
    for x, y in positions:
        position_counts[(x, y)] += 1

    # Fill grid with counts
    for (x, y), count in position_counts.items():
        grid[y][x] = str(count) if count < 10 else '*'

    # Print grid
    for row in grid:
        print(''.join(row))
    print()

def part1(input):
    robots = parse_input(input)
    final_positions = calculate_final_positions(robots, 100, 101, 103)
    return calculate_safety_factor(final_positions, 101, 103)

def part2(input):
    robots = parse_input(input)
    width, height = 101, 103
    total_robots = len(robots)

    print(f"Searching for solid vertical lines containing at least {total_robots * 0.05:.0f} robots...")
    for time in range(width * height):

        positions = calculate_final_positions(robots, time, width, height)
        found_line, x = check_vertical_line(positions, width, height, total_robots)

        if found_line:
            print_grid(positions, width, height)
            return time

    return None

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")