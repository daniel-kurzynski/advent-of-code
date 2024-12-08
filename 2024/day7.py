from aocd import get_data, submit
from itertools import product

# data = "190: 10 19\n3267: 81 40 27\n83: 17 5\n156: 15 6\n7290: 6 8 6 15\n161011: 16 10 13\n192: 17 8 14\n21037: 9 7 18 13\n292: 11 6 16 20"
data = get_data(day=7, year=2024)

def parse_data(input):
    rules = []
    for line in input.split('\n'):
        expected, numbers = line.split(': ')
        expected = int(expected)
        numbers = [int(x) for x in numbers.split()]
        rules.append((expected, numbers))
    return rules

def evaluate_expression(numbers, operators, expected):
    result = numbers[0]
    for i, op in enumerate(operators):
        if result > expected:
            return None
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
        else:  # concatenation operator ||
            result = int(str(result) + str(numbers[i + 1]))
    return result

def solve_part(rules, operators):
    total = 0
    for expected, numbers in rules:
        possible = False
        for ops in product(operators, repeat=len(numbers)-1):
            result = evaluate_expression(numbers, ops, expected)
            if result == expected:
                possible = True
                break
        if possible:
            total += expected
    return total

def part1(rules):
    return solve_part(rules, ['+', '*'])

def part2(rules):
    return solve_part(rules, ['+', '*', '||'])

rules = parse_data(data)
print(f"Part 1: {part1(rules)}")
print(f"Part 2: {part2(rules)}")