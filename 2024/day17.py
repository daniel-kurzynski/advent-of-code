from aocd import get_data, submit

data = "Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,3,5,4,3,0"  # Example data from puzzle
data = get_data(day=17, year=2024)

def parse_input(data):
    registers_section, program_section = data.split("\n\nProgram: ")

    registers = {}
    for line in registers_section.split("\n"):
        register, value = line.split(": ")
        registers[register[-1]] = int(value)

    numbers = [int(x) for x in program_section.split(",")]
    program = list(zip(numbers[::2], numbers[1::2]))

    return registers, program

def get_combo_value(operand, registers):
    if operand <= 3:  # literal 0-3
        return operand
    elif operand == 4:  # register A
        return registers['A']
    elif operand == 5:  # register B
        return registers['B']
    elif operand == 6:  # register C
        return registers['C']
    return None  # operand 7 is reserved

def execute_program(registers, program):
    outputs = []
    ip = 0  # instruction pointer

    while ip < len(program):
        opcode, operand = program[ip]

        if opcode == 0:  # adv
            power = get_combo_value(operand, registers)
            registers['A'] = registers['A'] // (2 ** power)
        elif opcode == 1:  # bxl
            registers['B'] ^= operand
        elif opcode == 2:  # bst
            registers['B'] = get_combo_value(operand, registers) % 8
        elif opcode == 3:  # jnz
            if registers['A'] != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            registers['B'] ^= registers['C']
        elif opcode == 5:  # out
            outputs.append(get_combo_value(operand, registers) % 8)
        elif opcode == 6:  # bdv
            power = get_combo_value(operand, registers)
            registers['B'] = registers['A'] // (2 ** power)
        elif opcode == 7:  # cdv
            power = get_combo_value(operand, registers)
            registers['C'] = registers['A'] // (2 ** power)

        ip += 1

    return outputs

def part1(data):
    registers, program = parse_input(data)
    outputs = execute_program(registers, program)
    return ','.join(str(x) for x in outputs)

def part2(data):
    registers, program = parse_input(data)

    expected_output = []
    for opcode, operand in program:
        expected_output.extend([opcode, operand])

    current_values = [0]

    for current_index in range(1, len(expected_output)+1):
        next_values = []
        for value in current_values:
            for value_a in range(value, value+8):
                registers['A'] = value_a
                outputs = execute_program(registers, program)
                if outputs == expected_output[-current_index:]:
                    next_values.append(value_a * 8)
                    if outputs == expected_output:
                        return value_a

        current_values = next_values

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
