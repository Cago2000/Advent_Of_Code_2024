import itertools
from enum import Enum

class Operator(Enum):
    ADD = 0
    MULTIPLY = 1
    CONCAT = 2
    def calculate(self, a: int, b: int):
        match self:
            case Operator.ADD:
                return a + b
            case Operator.MULTIPLY:
                return a * b
            case Operator.CONCAT:
                a, b = str(a), str(b)
                return int(a+b)

def main():
    all_operators = list(Operator)
    path = 'calibration_equations.txt'
    calibration_equations_file = open(path, 'r')
    equations = {}

    for equation_id, line in enumerate(calibration_equations_file):
        elements = line.split()
        equation_result = int(elements[0][:-1])
        equation_term = list(map(int, elements[1:]))
        equation = {
            "result": equation_result,
            "terms": equation_term,
            "operators": []
        }
        equations[equation_id] = equation

    total_sum = 0
    for equation_id in equations:
        equation = equations[equation_id]
        terms_size = len(equation["terms"])
        operator_combinations = list(itertools.product(all_operators, repeat=terms_size-1))
        is_equation_true = False
        cur_result = 0
        for operators in operator_combinations:
            cur_result = 0
            term_pairs = itertools.pairwise(equation["terms"])
            first_pair = True
            for (term_pair, operator) in zip(term_pairs, operators):
                a, b = term_pair
                if not first_pair:
                    a = cur_result
                else:
                    first_pair = False

                cur_result = operator.calculate(a, b)

            if cur_result == equation["result"]:
                is_equation_true = True
                break
        if is_equation_true:
            total_sum += cur_result

    print(f'total sum: {total_sum}')
if __name__ == "__main__":
    main()