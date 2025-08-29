import re
from enum import Enum

class Instruction(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

    def __str__(self):
        return self.name

    def get_function(self):
        match self:
            case self.ADV:
                def division(debugger, numerator, denominator):
                    debugger["a"] = int(numerator/denominator)
                    return debugger
                return division

            case self.BXL:
                def bitwise_xor(debugger, a, b):
                    debugger["b"] = a^b
                    return debugger
                return bitwise_xor

            case self.BST:
                def modulo(debugger, operand_value):
                    debugger["b"] = operand_value%8
                    return debugger
                return modulo

            case self.JNZ:
                def jump(debugger, instruction_pointer, operand):
                    if debugger["a"] == 0:
                        return instruction_pointer
                    instruction_pointer = operand
                    return instruction_pointer-2
                return jump

            case self.BXC:
                def register_bitwise_xor(debugger):
                    debugger["b"] = debugger["b"] ^ debugger["c"]
                    return debugger
                return register_bitwise_xor

            case self.OUT:
                def output(operand_value):
                    return operand_value%8
                return output

            case self.BDV:
                def division(debugger, numerator, denominator):
                    debugger["b"] = int(numerator/denominator)
                    return debugger
                return division

            case self.CDV:
                def division(debugger, numerator, denominator):
                    debugger["c"] = int(numerator/denominator)
                    return debugger
                return division


def main():
    data = load_file("debugger.txt")
    debugger = create_debugger(data)
    output = run_program(debugger)
    print(f'output: {",".join(list(map(str, output)))}')


def load_file(path: str):
    file = open(path, 'r')
    data = []
    for line in file:
        if line == "\n":
            continue
        line = line.removesuffix("\n")
        data.append(line)
    return data

def create_debugger(data: list[str]):

    register_a = int(re.findall(r'-?\d+', data[0])[0])
    register_b = int(re.findall(r'-?\d+', data[1])[0])
    register_c = int(re.findall(r'-?\d+', data[2])[0])
    program = list(map(int, re.findall(r'-?\d+', data[3])))

    debugger = {
        "a": register_a,
        "b": register_b,
        "c": register_c,
        "program": program
    }
    return debugger

def run_program(debugger: dict):
    program = debugger["program"]
    instruction_pointer = 0
    output = []
    while instruction_pointer < len(program)-1:
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer+1]
        instruction = Instruction(opcode)
        function = instruction.get_function()

        match instruction:
            case Instruction.ADV:
                operand_value = get_operand_value(debugger, operand)
                debugger = function(debugger, debugger["a"], 2**operand_value)
            case Instruction.BXL:
                debugger = function(debugger, debugger["b"], operand)
            case Instruction.BST:
                operand_value = get_operand_value(debugger, operand)
                debugger = function(debugger, operand_value)
            case Instruction.JNZ:
                instruction_pointer = function(debugger, instruction_pointer, operand)
            case Instruction.BXC:
                debugger = function(debugger)
            case Instruction.OUT:
                operand_value = get_operand_value(debugger, operand)
                output_value = function(operand_value)
                output.append(output_value)
            case Instruction.BDV:
                operand_value = get_operand_value(debugger, operand)
                debugger = function(debugger, debugger["a"], 2**operand_value)
            case Instruction.CDV:
                operand_value = get_operand_value(debugger, operand)
                debugger = function(debugger, debugger["a"], 2**operand_value)

        instruction_pointer += 2
    return output



def get_operand_value(debugger: dict, operand: int):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return debugger["a"]
        case 5:
            return debugger["b"]
        case 6:
            return debugger["c"]
        case 7:
            raise ValueError("Operand 7 is invalid as a value")



def find_a(debugger):
    program = debugger["program"]
    n = len(program)
    candidates = [0]

    for i in range(n):
        expected = program[n - 1 - i]
        new_candidates = []
        for j in candidates:
            for k in range(8):
                candidate = (j << 3) | k
                test_debugger = dict(debugger)
                test_debugger["a"] = candidate
                output = run_program(test_debugger)
                if len(output) >= n - i and output[n - 1 - i] == expected:
                    new_candidates.append(candidate)
        candidates = new_candidates
    return min(candidates) if candidates else None

if __name__ == "__main__":
    main()