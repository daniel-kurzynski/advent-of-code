from aocd import get_data, submit

data = get_data(day=1, year=2025)

def preprocess(raw: str):
    return [(line[0], int(line[1:])) for line in raw.strip().split('\n')]

def simulate(directions):
    position = 50
    stopping = 0
    stopping_or_passing = 0

    for direction, amount in directions:
        old_position = position
        sign = 1 if direction == 'R' else -1
        position = position + sign * amount

        stopping_or_passing += abs(position // 100)

        position = position % 100

        if old_position == 0 and direction == 'L':
            stopping_or_passing -= 1

        if position == 0 and direction == 'R':
            stopping_or_passing -= 1

        if position == 0:
            stopping += 1
            stopping_or_passing += 1

    return stopping, stopping_or_passing

directions = preprocess(data)
stopping, stopping_or_passing = simulate(directions)

print('Part 1:', stopping)
print('Part 2:', stopping_or_passing)
