from cli import create_day_cli


def parse_input(path):
    equations = []
    with open(path) as f:
        for line in f:
            lhs, rhs = line.split(":")
            equations.append((int(lhs), [int(x) for x in rhs.split()]))
    return equations


def part1(equations):
    op_funcs = {
        "+": lambda x, y: int(x) + int(y),
        "*": lambda x, y: int(x) * int(y),
    }

    result = 0
    for lhs, operands in equations:
        result += lhs if backtrack(lhs, operands, 0, 0, op_funcs) else 0
    return result


def part2(equations):
    op_funcs = {
        "+": lambda x, y: int(x) + int(y),
        "*": lambda x, y: int(x) * int(y),
        "||": lambda x, y: str(x) + str(y),
    }

    result = 0
    for lhs, operands in equations:
        result += lhs if backtrack(lhs, operands, 0, 0, op_funcs) else 0
    return result


def backtrack(lhs, operands, idx, running, op_funcs):
    if int(running) > lhs:
        return False
    if idx >= len(operands):
        return int(running) == lhs
    for _, func in op_funcs.items():
        updated = func(running, operands[idx])
        if backtrack(lhs, operands, idx + 1, updated, op_funcs):
            return True
    return False


app = create_day_cli(day_number=7, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(parse_input("data/day7.txt")))
    print(part2(parse_input("data/day7.txt")))
