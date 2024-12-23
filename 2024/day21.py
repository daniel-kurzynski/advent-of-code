from aocd import get_data, submit
from collections import defaultdict, deque
from functools import cache

data = "029A\n980A\n179A\n456A\n379A"  # Example data
data = get_data(day=21, year=2024)

# Keypad layouts
DIRECTIONAL_KEYPAD = {
    (0, 1): '^',
    (0, 2): 'A',
    (1, 0): '<',
    (1, 1): 'v',
    (1, 2): '>'
}

NUMERIC_KEYPAD = {
    (0, 0): '7',
    (0, 1): '8',
    (0, 2): '9',
    (1, 0): '4',
    (1, 1): '5',
    (1, 2): '6',
    (2, 0): '1',
    (2, 1): '2',
    (2, 2): '3',
    (3, 1): '0',
    (3, 2): 'A'
}

DIRECTIONAL_KEYPAD_POSITION = {v: k for k, v in DIRECTIONAL_KEYPAD.items()}
NUMERIC_KEYPAD_POSITION = {v: k for k, v in NUMERIC_KEYPAD.items()}

def find_shortest_sequences_single_layer(from_key, to_key, keypad, keypad_positions):
    from_pos = keypad_positions[from_key]
    to_pos = keypad_positions[to_key]

    queue = deque([(from_pos, [])])
    shortest_sequences = []
    min_length = float('inf')

    while queue:
        pos, path = queue.popleft()

        if pos == to_pos:
            if len(path) < min_length:
                shortest_sequences = [path + ["A"]]
                min_length = len(path)
            elif len(path) == min_length:
                shortest_sequences.append(path + ["A"])
            continue

        if len(path) >= min_length:
            continue

        x, y = pos
        moves = [
            ((x-1, y), '^'),
            ((x+1, y), 'v'),
            ((x, y-1), '<'),
            ((x, y+1), '>')
        ]

        for next_pos, direction in moves:
            if next_pos in keypad:
                queue.append((next_pos, path + [direction]))

    return shortest_sequences

@cache
def find_shortest_sequences_single_layer_on_numpad(from_key, to_key):
    return find_shortest_sequences_single_layer(from_key, to_key, NUMERIC_KEYPAD, NUMERIC_KEYPAD_POSITION)

@cache
def find_shortest_sequences_single_layer_on_directional_keypad(from_key, to_key):
    return find_shortest_sequences_single_layer(from_key, to_key, DIRECTIONAL_KEYPAD, DIRECTIONAL_KEYPAD_POSITION)

@cache
def length_of_shortest_sequences_directional(from_key, to_key, num_directional_layers=1):
    sequences = find_shortest_sequences_single_layer_on_directional_keypad(from_key, to_key)

    if num_directional_layers == 1:
        return len(sequences[0])

    min_length = float('inf')
    for sequence in sequences:
        initial_sequence = ["A"] + sequence

        sum = 0
        for i in range(len(initial_sequence) - 1):
            length = length_of_shortest_sequences_directional(initial_sequence[i], initial_sequence[i + 1], num_directional_layers-1)
            sum += length

        if sum < min_length:
            min_length = sum

    return min_length

def length_of_shortest_sequences_directional_sequence(initial_sequence, num_directional_layers):
    if num_directional_layers == 0:
        return len(initial_sequence)

    initial_sequence = ["A"] + initial_sequence
    sum = 0
    for i in range(len(initial_sequence) - 1):
        length = length_of_shortest_sequences_directional(initial_sequence[i], initial_sequence[i + 1], num_directional_layers)
        sum += length
    return sum

def length_of_shortest_sequences_numpad(code, num_directional_layers=1):
    code = "A" + code
    sum = 0
    for i in range(len(code) - 1):
        sequences = find_shortest_sequences_single_layer_on_numpad(code[i], code[i + 1])

        min_length = float('inf')
        for sequence in sequences:
            length = length_of_shortest_sequences_directional_sequence(sequence, num_directional_layers-1)
            if length < min_length:
                min_length = length
        sum += min_length

    return sum

def get_numeric_value(code):
    numeric_part = ''.join(c for c in code if c.isdigit())
    return int(numeric_part)

def complexity_of_code(code, num_directional_layers):
    return length_of_shortest_sequences_numpad(code, num_directional_layers) * get_numeric_value(code)

def solve(input, num_directional_layers):
    codes = input.strip().split('\n')
    complexity = 0
    for code in codes:
        code_complexity = complexity_of_code(code, num_directional_layers)
        complexity += code_complexity

    return complexity

print(f"Part 1: {solve(data, 3)}")
print(f"Part 2: {solve(data, 26)}")