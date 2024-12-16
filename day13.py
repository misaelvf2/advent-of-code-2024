import math
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
        # Try the maximum possible number of B presses possible
        b_presses = min(
            machine.Prize_X // machine.B_X, machine.Prize_Y // machine.B_Y, 100
        )
        while not valid_solution(b_presses, machine) and b_presses >= 0:
            b_presses -= 1
        if b_presses >= 0:
            a_presses = (machine.Prize_X - b_presses * machine.B_X) // machine.A_X
            cost = (b_presses * 1) + (a_presses * 3)
            tokens += cost
    return tokens


def valid_solution(b_presses, machine: Machine):
    remaining_x = machine.Prize_X - b_presses * machine.B_X
    remaining_y = machine.Prize_Y - b_presses * machine.B_Y
    a_presses_x = remaining_x // machine.A_X
    a_presses_y = remaining_y // machine.A_Y
    return (
        a_presses_x == a_presses_y
        and remaining_x % a_presses_x == 0
        and remaining_y % a_presses_y == 0
    )


def part2(machines):
    pass


if __name__ == "__main__":
    print(part1(parse_input("data/day13.txt")))
    print(part2(parse_input("data/day13.txt")))
