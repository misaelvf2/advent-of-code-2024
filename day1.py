from collections import Counter

from cli import create_day_cli


def parse_input(path):
    left = []
    right = []
    with open(path) as f:
        for line in f:
            left_num, right_num = map(int, line.split())
            left.append(left_num)
            right.append(right_num)
    return left, right


def part1(left, right):
    return sum([abs(x - y) for (x, y) in zip(sorted(left), sorted(right))])


def part2(left, right):
    return sum([num * Counter(right)[num] for num in left])


app = create_day_cli(day_number=1, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    app()
