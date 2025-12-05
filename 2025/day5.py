from aocd import get_data, submit

# data = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32"
data = get_data(day=5, year=2025)

def preprocess(raw: str):
    ranges_part, ids_part = raw.split('\n\n')
    ranges = [(int(line.split('-')[0]), int(line.split('-')[1])) for line in ranges_part.strip().split('\n')]
    ids = [int(x) for x in ids_part.strip().split('\n')]
    return join(ranges), ids

def join(ranges):
    ranges = sorted(ranges)
    if not ranges:
        return []

    joined = []
    current_start, current_end = ranges[0]

    for next_start, next_end in ranges[1:]:
        if current_end >= next_start - 1:
            current_end = max(current_end, next_end)
        else:
            joined.append((current_start, current_end))
            current_start, current_end = next_start, next_end

    joined.append((current_start, current_end))
    return joined

def solve_part1():
    ranges, ids = preprocess(data)
    return sum(1 for id_val in ids if any(start <= id_val <= end for start, end in ranges))

def solve_part2():
    ranges, ids = preprocess(data)
    return sum(end - start + 1 for start, end in ranges)

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())