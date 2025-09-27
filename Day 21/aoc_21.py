import string
from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other: 'Position') -> 'Position':
        max_x, max_y = 2, 3
        new_x = min(max(self.x + other.x, 0), max_x)
        new_y = min(max(self.y + other.y, 0), max_y)
        return Position(new_x, new_y)

@dataclass
class Keypad:
    cursor = Position(2, 3)
    keypad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["3", "2", "1"],
        ["x", "0", "A"]
    ]

    def __str__(self) -> str:
        rows = []
        for y, row in enumerate(self.keypad):
            display_row = []
            for x, val in enumerate(row):
                if self.cursor.x == x and self.cursor.y == y:
                    display_row.append(f"[{val}]")
                else:
                    display_row.append(f" {val} ")
            rows.append(" ".join(display_row))
        return "\n".join(rows)

    def get_position_by_symbol(self, symbol: string):
        for y, _ in enumerate(self.keypad):
            for x, _ in enumerate(self.keypad[y]):
                if self.keypad[y][x] == symbol:
                    return Position(x, y)

    def execute_sequence(self, symbol: string):
        symbol_position = self.get_position_by_symbol(symbol)
        sequence = self.get_dpad_sequence(symbol_position)
        self.cursor = symbol_position
        sequence += "A"
        return sequence

    def get_dpad_sequence(self, destination: Position):
        dx, dy = destination.x-self.cursor.x, destination.y-self.cursor.y
        inputs = []
        if dy < 0:
            for y in range(0, abs(dy)):
                inputs.append("^")
            if dx < 0:
                for x in range(0, abs(dx)):
                    inputs.append("<")
            if dx > 0:
                for x in range(0, abs(dx)):
                    inputs.append(">")
        if dy > 0:
            if dx < 0:
                for x in range(0, abs(dx)):
                    inputs.append("<")
            if dx > 0:
                for x in range(0, abs(dx)):
                    inputs.append(">")
            for y in range(0, abs(dy)):
                inputs.append("v")
        if dy == 0:
            if dx < 0:
                for x in range(0, abs(dx)):
                    inputs.append("<")
            if dx > 0:
                for x in range(0, abs(dx)):
                    inputs.append(">")
        return "".join(inputs)

@dataclass
class DPad:
    cursor = Position(2, 0)
    dpad = [
        ["x", "^", "A"],
        ["<", "v", ">"],
    ]

    def __str__(self) -> str:
        rows = []
        for y, row in enumerate(self.dpad):
            display_row = []
            for x, val in enumerate(row):
                if self.cursor.x == x and self.cursor.y == y:
                    display_row.append(f"[{val}]")
                else:
                    display_row.append(f" {val} ")
            rows.append(" ".join(display_row))
        return "\n".join(rows)

    def get_position_by_symbol(self, symbol: string):
        for y, _ in enumerate(self.dpad):
            for x, _ in enumerate(self.dpad[y]):
                if self.dpad[y][x] == symbol:
                    return Position(x, y)

    def execute_sequence(self, symbol: string):
        symbol_position = self.get_position_by_symbol(symbol)
        sequence = self.get_dpad_sequence(symbol_position)
        sequence += "A"
        self.cursor = symbol_position
        return sequence

    def get_dpad_sequence(self, destination: Position):
        dx, dy = destination.x-self.cursor.x, destination.y-self.cursor.y
        inputs = []
        if dy < 0:
            if dx < 0:
                for x in range(0, abs(dx)):
                    inputs.append("<")
            if dx > 0:
                for x in range(0, abs(dx)):
                    inputs.append(">")
            for y in range(0, abs(dy)):
                inputs.append("^")
        if dy > 0:
            for y in range(0, abs(dy)):
                inputs.append("v")
                if dx < 0:
                    for x in range(0, abs(dx)):
                        inputs.append("<")
                if dx > 0:
                    for x in range(0, abs(dx)):
                        inputs.append(">")
        if dy == 0:
            if dx < 0:
                for x in range(0, abs(dx)):
                    inputs.append("<")
            if dx > 0:
                for x in range(0, abs(dx)):
                    inputs.append(">")
        return "".join(inputs)

def main():

    keypad = Keypad()
    dpad1 = DPad()
    dpad2 = DPad()
    dpad3 = DPad()
    data = load_file("input_example.txt")

    inputs = []
    print(f'dpad1: \n{dpad1}')
    print("----------------")
    for line in data:
        for k in line:
            k_seq = keypad.execute_sequence(k)
            print(f'keypad: \n{keypad}')
            print(k_seq)
            print("----------------")
            print()
            for d1 in k_seq:
                d1_seq = dpad1.execute_sequence(d1)
                print(f'dpad1: \n{dpad1}')
                print(d1_seq)
                print("----------------")
                print()
                inputs.append(d1_seq)
                for d2 in d1_seq:
                    d2_seq = dpad2.execute_sequence(d2)
                    print(f'dpad2: \n{dpad2}')
                    print(d2_seq)
                    print("----------------")
                    print()
                    for d3 in d2_seq:
                        d3_seq = dpad3.execute_sequence(d3)
                        print(f'dpad3: \n{dpad3}')
                        print(d3_seq)
                        print("----------------")
                        print()
                        inputs.append(d3_seq)
    print("".join(inputs))

def load_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    main()