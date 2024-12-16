from aocd import get_data, submit
import re

data = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279'''  # Example data
data = get_data(day=13, year=2024)

def parse_data(input, add_offset=False):
    machines = []
    sections = input.split('\n\n')
    OFFSET = 10_000_000_000_000 if add_offset else 0

    for section in sections:
        lines = section.split('\n')
        # Extract numbers using regex
        prize_coords = re.findall(r'X=(\d+), Y=(\d+)', lines[2])[0]
        button_a = re.findall(r'X\+(\d+), Y\+(\d+)', lines[0])[0]
        button_b = re.findall(r'X\+(\d+), Y\+(\d+)', lines[1])[0]

        # Convert to integers and create tuples
        prize = (int(prize_coords[0]) + OFFSET, int(prize_coords[1]) + OFFSET)
        move_a = (int(button_a[0]), int(button_a[1]))
        move_b = (int(button_b[0]), int(button_b[1]))

        machines.append((prize, move_a, move_b))

    return machines

def solve_equations(prize, button_a, button_b, max_presses=None):
    denominator = (button_a[1] * button_b[0] - button_a[0] * button_b[1])
    if denominator == 0:
        return None  # No solution exists

    A = (prize[1] * button_b[0] - prize[0] * button_b[1]) / denominator
    B = (prize[0] - A * button_a[0]) / button_b[0]

    # Check if A and B are positive integers and less than max_presses if specified
    if A >= 0 and B >= 0 and A.is_integer() and B.is_integer():
        if max_presses is None or (A <= max_presses and B <= max_presses):
            return (int(A), int(B))
    return None

def calculate_tokens(a_presses, b_presses):
    return a_presses * 3 + b_presses * 1

def part1(input):
    machines = parse_data(input)
    total_tokens = 0
    possible_wins = 0

    for prize, button_a, button_b in machines:
        solution = solve_equations(prize, button_a, button_b, max_presses=100)
        if solution:
            possible_wins += 1
            total_tokens += calculate_tokens(*solution)

    return total_tokens if possible_wins > 0 else "No solutions found"

def part2(input):
    machines = parse_data(input, add_offset=True)
    total_tokens = 0
    possible_wins = 0

    for prize, button_a, button_b in machines:
        solution = solve_equations(prize, button_a, button_b)
        if solution:
            possible_wins += 1
            total_tokens += calculate_tokens(*solution)

    return total_tokens if possible_wins > 0 else "No solutions found"

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")