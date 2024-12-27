import copy

from aocd import get_data, submit
from collections import defaultdict
from itertools import combinations

data = get_data(day=24, year=2024)

def parse_data(input):
    sections = input.strip().split('\n\n')
    initial_section = sections[0].strip().split('\n')
    gates_section = sections[1].strip().split('\n')

    initial_values = {}
    gates = {}
    connections = {}

    # Parse initial values and setup their connections (empty list)
    for line in initial_section:
        wire, value = line.split(': ')
        initial_values[wire] = int(value)
        connections[wire] = []

    # Parse gates
    for line in gates_section:
        inputs, output = line.split(' -> ')
        parts = inputs.split()

        # Store gate with its operation and inputs
        operation = parts[1]
        in1, in2 = sorted([parts[0], parts[2]])
        gates[output] = (operation, in1, in2)

        # Add gate to connections of input wires
        if in1 not in connections:
            connections[in1] = []
        if in2 not in connections:
            connections[in2] = []

        if output not in connections:
            connections[output] = []

        connections[in1].append(output)
        connections[in2].append(output)

    return initial_values, gates, connections

def compute_gate(operation, value1, value2):
    if operation == 'AND':
        return value1 & value2
    elif operation == 'OR':
        return value1 | value2
    elif operation == 'XOR':
        return value1 ^ value2
    return None

def compute_circuit(initial_values, gates, connections):
    current_values = initial_values.copy()

    def propagate(wire, value):
        current_values[wire] = value

        if wire in connections:
            for gate_name in connections[wire]:
                operation, in1, in2 = gates[gate_name]

                # Check if both inputs are available
                if in1 in current_values and in2 in current_values:
                    output_value = compute_gate(operation, current_values[in1], current_values[in2])
                    if output_value is not None and gate_name not in current_values:
                        propagate(gate_name, output_value)

    # Start propagation from all initial values
    for wire, value in initial_values.items():
        propagate(wire, value)

    return current_values

def part1(initial_values, gates, connections):
    current_values = compute_circuit(initial_values, gates, connections)

    z_wires = sorted([wire for wire in current_values if wire.startswith('z')], reverse=True)
    return int(''.join(str(current_values[wire]) for wire in z_wires), 2)

def build_formulas(gates):
    formulas = {}  # formula string -> gate name

    for gate in gates:
        operation, in1, in2 = gates[gate]
        formulas[f"{in1} {operation} {in2}"] = gate

    return formulas

def swap_gates(gates, gate1, gate2):
    new_gates = gates.copy()

    # Swap the gate values
    new_gates[gate1], new_gates[gate2] = new_gates[gate2], new_gates[gate1]

    return new_gates

def check_adder_formulas(gates):
    formulas = build_formulas(gates)
    carry_gate = None

    z_gates = sorted([g for g in gates if g.startswith('z')])
    for index, z_gate in enumerate(z_gates):

        if index == len(z_gates) - 1:
            if carry_gate != z_gate:
                #print(f"Expected gate {z_gate} for carry output, got {carry_gate}")
                return (z_gate, carry_gate)
            break

        zindex = int(z_gate[1:])
        sum_formular = f"x{zindex:02} XOR y{zindex:02}"
        half_carry_formular = f"x{zindex:02} AND y{zindex:02}"

        half_sum_gate = formulas[sum_formular]
        half_carry_gate = formulas[half_carry_formular]

        if carry_gate is None:
            if half_sum_gate != z_gate:
                #print(f"Expected gate {z_gate} for sum formula {sum_formular}, got {half_sum_gate}")
                return (z_gate, half_sum_gate)

            carry_gate = half_carry_gate
        else:
            in1, in2 = sorted([carry_gate, half_sum_gate])
            full_sum_formular = f"{in1} XOR {in2}"

            if full_sum_formular not in formulas:
                _, actual_in1, actual_in2 = gates[z_gate]
                unexpected = {actual_in1, actual_in2} - {in1, in2}
                missing = {in1, in2} - {actual_in1, actual_in2}
                assert len(unexpected) == 1 and len(missing) == 1
                pair = missing.pop(), unexpected.pop()
                #print(f"Expected gate {pair[0]} for sum formula {full_sum_formular}, got {pair[1]}")
                return pair

            full_sum_gate = formulas[full_sum_formular]

            if full_sum_gate != z_gate:
                #print(f"Expected gate {z_gate} for sum formula {sum_formular}, got {full_sum_gate}")
                return (z_gate, full_sum_gate)

            in1, in2 = sorted([carry_gate, half_sum_gate])
            carry_formular_op1 = f"{in1} AND {in2}"
            carry_op1_gate = formulas[carry_formular_op1]

            in1, in2 = sorted([half_carry_gate, carry_op1_gate])
            carry_formular = f"{in1} OR {in2}"
            carry_gate = formulas[carry_formular]

    return None

def part2(gates):
    current_gates = copy.deepcopy(gates)
    gates_to_swap = []

    while True:
        pair = check_adder_formulas(current_gates)
        if pair:
            gates_to_swap.extend(pair)
            current_gates = swap_gates(current_gates, *pair)
        else:
            break

    return ",".join(sorted(gates_to_swap))

initial_values, gates, connections = parse_data(data)

print(f"Part 1: {part1(initial_values, gates, connections)}")
print(f"Part 2: {part2(gates)}")