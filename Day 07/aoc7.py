import functools
import itertools
from enum import Enum
from typing import Tuple

class Operator(Enum):
    ADD = 0
    MULTIPLY = 1
    CONCAT = 2
    def calculate(self, a: int, b: int) -> int:
        match self:
            case Operator.ADD: return a + b
            case Operator.MULTIPLY: return a * b
            case Operator.CONCAT:
                a, b = str(a), str(b)
                return int(a+b)

def evaluate(acc: int, operator_value_pair: Tuple[Operator, int]) -> int:
    operator, next_val = operator_value_pair
    return operator.calculate(acc, next_val)

def main():
    all_operators = list(Operator)
    calibration_equations_file = open('calibration_equations_example.txt', 'r')
    equations = {}

    for equation_id, line in enumerate(calibration_equations_file):
        elements = line.split()
        equation = {
            "result": int(elements[0][:-1]),
            "terms": list(map(int, elements[1:])),
            "operators": []
        }
        equations[equation_id] = equation

    true_equations = []
    total_sum = 0
    for equation_id in equations:
        equation = equations[equation_id]
        terms_size = len(equation["terms"])
        operator_combinations = list(itertools.product(all_operators, repeat=terms_size-1))
        is_equation_true = False
        cur_result = 0
        for operators in operator_combinations:
            cur_result = functools.reduce(evaluate, zip(operators, equation["terms"][1:]), equation["terms"][0])
            if cur_result == equation["result"]:
                equation["operators"] = operators
                true_equations.append(equation)
                is_equation_true = True
                break
        if is_equation_true:
            total_sum += cur_result

    print(f'total sum: {total_sum}')
    print(f'true equations:')
    for equation in true_equations:
        print(equation)

if __name__ == "__main__":
    main()