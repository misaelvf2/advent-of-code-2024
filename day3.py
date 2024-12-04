import re

from cli import create_day_cli


def parse_input(path):
    with open(path) as f:
        return f.read()


def part1(instructions):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    return sum(
        int(mul.group(1)) * int(mul.group(2))
        for mul in re.finditer(pattern, instructions)
    )


def part2(instructions):
    result = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)"

    is_on = True
    for instruction in re.finditer(pattern, instructions):
        match instruction.group():
            case "do()":
                is_on = True
            case "don't()":
                is_on = False
            case _:
                if is_on:
                    result += int(instruction.group(1)) * int(instruction.group(2))

    return result


app = create_day_cli(day_number=3, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    app()
