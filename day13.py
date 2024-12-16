import re
from collections import namedtuple

Machine = namedtuple("Machine", ["A_X", "A_Y", "B_X", "B_Y", "Prize_X", "Prize_Y"])


def parse_input(path):
    button_pattern = r"X\+(\d+), Y\+(\d+)"
    prize_pattern = r"X=(\d+), Y=(\d+)"
    machines = []
    with open(path) as f:
        lines = [line.strip() for line in f]
        i = 0
        while i < len(lines):
            machine = {}
            button_match = re.search(button_pattern, lines[i])
            if button_match:
                machine["A_X"] = int(button_match.group(1))
                machine["A_Y"] = int(button_match.group(2))
            button_match = re.search(button_pattern, lines[i + 1])
            if button_match:
                machine["B_X"] = int(button_match.group(1))
                machine["B_Y"] = int(button_match.group(2))
            prize_match = re.search(prize_pattern, lines[i + 2])
            if prize_match:
                machine["Prize_X"] = int(prize_match.group(1))
                machine["Prize_Y"] = int(prize_match.group(2))
            machines.append(Machine(**machine))
            i += 4
    return machines


def part1(machines: list[Machine]):
    tokens = 0
    for machine in machines:
        a_presses = (
            (machine.B_X * machine.Prize_Y) - (machine.Prize_X * machine.B_Y)
        ) / ((machine.A_Y * machine.B_X) - machine.A_X * machine.B_Y)
        b_presses = (machine.Prize_X - (a_presses * machine.A_X)) / machine.B_X
        a_presses = int(a_presses)
        b_presses = int(b_presses)
        if valid_solution(a_presses, b_presses, machine):
            cost = 3 * a_presses + b_presses
            tokens += cost
    return tokens


def part2(machines: list[Machine]):
    tokens = 0
    for machine in machines:
        a_presses = (
            (machine.B_X * (machine.Prize_Y + 10000000000000))
            - ((machine.Prize_X + 10000000000000) * machine.B_Y)
        ) / ((machine.A_Y * machine.B_X) - machine.A_X * machine.B_Y)
        b_presses = (
            machine.Prize_X + 10000000000000 - (a_presses * machine.A_X)
        ) / machine.B_X
        a_presses = int(a_presses)
        b_presses = int(b_presses)
        if valid_solution(a_presses, b_presses, machine, part_b=True):
            cost = 3 * a_presses + b_presses
            tokens += cost
    return tokens


def valid_solution(a_presses, b_presses, machine: Machine, part_b: bool = False):
    if not part_b:
        if not (0 <= a_presses <= 100 and 0 <= b_presses <= 100):
            return False
        satisfies_X = (
            a_presses * machine.A_X + b_presses * machine.B_X == machine.Prize_X
        )
        satisfies_Y = (
            a_presses * machine.A_Y + b_presses * machine.B_Y == machine.Prize_Y
        )
    else:
        satisfies_X = (
            a_presses * machine.A_X + b_presses * machine.B_X
            == machine.Prize_X + 10000000000000
        )
        satisfies_Y = (
            a_presses * machine.A_Y + b_presses * machine.B_Y
            == machine.Prize_Y + 10000000000000
        )
    return satisfies_X and satisfies_Y


if __name__ == "__main__":
    print(part1(parse_input("data/day13.txt")))
    print(part2(parse_input("data/day13.txt")))
