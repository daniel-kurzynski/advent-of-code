from aocd import get_data, submit
import numpy as np

# data = "..@@.@@@@.\n@@@.@.@.@@\n@@@@@.@.@@\n@.@@@@..@.\n@@.@@@@.@@\n.@@@@@@@.@\n.@.@.@.@@@\n@.@@@.@@@@\n.@@@@@@@@.\n@.@.@@@.@."
data = get_data(day=4, year=2025)

def preprocess(raw: str):
    lines = raw.strip().split('\n')
    return np.array([list(line) for line in lines])

def solve(updateState=False):
    """
    Args:
        updateState: If False (part 1), count @ with <4 neighbors once.
                     If True (part 2), iteratively remove @ and update state.
    """
    grid = preprocess(data)
    total_count = 0

    while True:
        rows, cols = grid.shape
        to_count = []

        for i in range(rows):
            for j in range(cols):
                if grid[i, j] == '@':
                    neighbors = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < rows and 0 <= nj < cols:
                                if grid[ni, nj] == '@':
                                    neighbors += 1

                    if neighbors < 4:
                        to_count.append((i, j))

        total_count += len(to_count)

        if not updateState:
            break

        if len(to_count) == 0:
            break

        for i, j in to_count:
            grid[i, j] = 'x'

    return total_count

print('Part 1:', solve(updateState=False))
print('Part 2:', solve(updateState=True))