import re
from sympy import symbols, Eq, linsolve

def main():
    claw_machine_data = load_file('claw_machines.txt')
    claw_machines = get_dict_from_data(claw_machine_data)
    for cm_id, claw_machine in claw_machines.items():
        solution = solve_equations(claw_machine["A"], claw_machine["B"], claw_machine["Prize"])
        claw_machines[cm_id]["Solution"] = solution
    total_tokens = calculate_tokens(claw_machines)
    print(total_tokens)
    for _, cm in claw_machines.items():
        print(cm)

def load_file(path: str):

    file = open(path, 'r')
    data = []
    for line in file:
        if line == "\n":
            continue
        data.append(line)
    return data

def get_dict_from_data(data: list[str]):
    i = 0
    claw_machines = {}
    claw_machine_index = 0
    while i < len(data):
        lines = data[i:i+3]
        for k, line in enumerate(lines):
            line = line.removesuffix("\n")
            lines[k] = line
        digits_a = re.split(r'\D+', lines[0])
        digits_b = re.split(r'\D+', lines[1])
        digits_prize = re.split(r'\D+', lines[2])
        claw_machine = {
            "A": (int(digits_a[1]), int(digits_a[2])),
            "B": (int(digits_b[1]), int(digits_b[2])),
            "Prize": (int(digits_prize[1]), int(digits_prize[2])),
            "Solution": (-1, -1),
        }
        claw_machines[claw_machine_index] = claw_machine
        claw_machine_index += 1
        i+=3
    return claw_machines

def solve_equations(a_button: tuple[int, int], b_button: tuple[int, int], prize: tuple[int, int]):
    a, b = symbols('a b', integer=True)
    ax, ay = a_button
    bx, by = b_button
    x_prize, y_prize = prize

    a_equation = Eq(ax * a + bx * b, x_prize)
    b_equation = Eq(ay * a + by * b, y_prize)

    solution = list(linsolve((a_equation, b_equation), (a, b)))
    a, b = solution[0]
    a, b = int(a), int(b)
    if a < 0 or a > 100 or b < 0 or b > 100:
        a, b = (0, 0)
    print(f'A: {a_button}, B: {b_button}')
    print(f'A: {ax} * {a} + {bx} * {b} = {x_prize}')
    print(f'B: {ay} * {a} + {by} * {b} = {y_prize}')
    print(f'Solution; {a, b}')
    return a, b

def calculate_tokens(claw_machines):
    total_tokens = 0
    for _, claw_machine in claw_machines.items():
        a, b = claw_machine["Solution"]
        total_tokens += a*3+b*1
    return total_tokens


if __name__ == "__main__":
    main()