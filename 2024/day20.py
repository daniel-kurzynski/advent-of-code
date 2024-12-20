from aocd import get_data, submit
from collections import deque

data,debug = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""", True  # Example data
data,debug = get_data(day=20, year=2024), False

def parse_input(data):
    grid = [list(line) for line in data.splitlines()]
    start = None
    end = None

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
                grid[i][j] = '.'
            elif grid[i][j] == 'E':
                end = (i, j)

    return grid, start, end

def calculate_distances(grid, end):
    rows = len(grid)
    cols = len(grid[0])
    distances = [[float('inf')] * cols for _ in range(rows)]

    # Start from end with distance 0
    queue = [(end, 0)]
    distances[end[0]][end[1]] = 0

    # BFS to calculate distances
    while queue:
        (x, y), dist = queue.pop(0)

        # Check all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy

            # Check bounds and if it's a path
            if (0 <= new_x < rows and
                    0 <= new_y < cols and
                    grid[new_x][new_y] == '.' and
                    distances[new_x][new_y] == float('inf')):

                distances[new_x][new_y] = dist + 1
                queue.append(((new_x, new_y), dist + 1))

    return distances

def find_cheats(grid, distances, max_cheat_distance):
    rows = len(grid)
    cols = len(grid[0])
    cheats = []

    # Check every position
    for x in range(rows):
        for y in range(cols):
            if distances[x][y] == float('inf'):
                continue

            start_dist = distances[x][y]

            # Check all positions reachable in 2 steps
            for dx1 in range(-max_cheat_distance, max_cheat_distance + 1):
                for dy1 in range(-max_cheat_distance, max_cheat_distance + 1):
                    distance = abs(dx1) + abs(dy1)
                    # Skip if not exactly 2 steps away (Manhattan distance)
                    if distance <= 1 or distance > max_cheat_distance:
                        continue

                    new_x, new_y = x + dx1, y + dy1

                    # Check bounds and if destination has a valid distance
                    if (0 <= new_x < rows and
                            0 <= new_y < cols and
                            distances[new_x][new_y] != float('inf') and
                            distances[new_x][new_y] < start_dist):

                        # Calculate time saved:
                        # Original distance minus (new distance + distance moves through wall)
                        time_saved = start_dist - (distances[new_x][new_y] + distance)

                        if time_saved > 0:
                            cheats.append(((x, y), (new_x, new_y), time_saved))

    return cheats


def print_histogram_cheats(cheats):
    # Group cheats by time saved
    savings_count = {}
    for _, _, saved in cheats:
        savings_count[saved] = savings_count.get(saved, 0) + 1

    # Print counts for each time saving
    for saved_time in sorted(savings_count.keys()):
        print(f"Part 2: There are {savings_count[saved_time]} cheats that save {saved_time} picoseconds.")


def part1(grid, distances):
    cheats = find_cheats(grid, distances, 2)
    if debug:
        print_histogram_cheats(cheats)

    # Count cheats that save at least 100 picoseconds
    return sum(1 for _, _, saved in cheats if saved >= 100)


def part2(grid, distances):
    cheats = find_cheats(grid, distances, 20)
    if debug:
        print_histogram_cheats(cheats)

    # Count cheats that save at least 100 picoseconds
    return sum(1 for _, _, saved in cheats if saved >= 100)


grid, start, end = parse_input(data)
distances = calculate_distances(grid, end)

print(f"Part 1: {part1(grid, distances)}")
print(f"Part 2: {part2(grid, distances)}")