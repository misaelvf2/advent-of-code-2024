import itertools

# from cli import create_day_cli


def parse_input(path):
    with open(path) as f:
        return [[int(x) for x in line.split()] for line in f]


def part1(reports: list):
    return sum(
        all(
            gradually_increasing(previous, current, lower_limit=1, upper_limit=3)
            for previous, current in itertools.pairwise(report)
        )
        or all(
            gradually_decreasing(previous, current, lower_limit=1, upper_limit=3)
            for previous, current in itertools.pairwise(report)
        )
        for report in reports
    )


def part2(reports: list):
    safe = 0
    for report in reports:
        for i in range(len(report)):
            if all(
                gradually_increasing(previous, current, lower_limit=1, upper_limit=3)
                for previous, current in itertools.pairwise(
                    report[:i] + report[i + 1 :]
                )
            ) or all(
                gradually_decreasing(previous, current, lower_limit=1, upper_limit=3)
                for previous, current in itertools.pairwise(
                    report[:i] + report[i + 1 :]
                )
            ):
                safe += 1
                break
    return safe


def gradually_increasing(x, y, lower_limit, upper_limit):
    return lower_limit <= x - y <= upper_limit


def gradually_decreasing(x, y, lower_limit, upper_limit):
    return lower_limit <= y - x <= upper_limit


# app = create_day_cli(day_number=2, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(parse_input("data/day2.txt")))
    print(part2(parse_input("data/day2.txt")))
