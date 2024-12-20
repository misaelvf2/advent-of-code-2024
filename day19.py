import functools


def parse_input(path):
    desired = []
    with open("data/day19.txt") as f:
        lines = f.readlines()
        patterns = [p.strip() for p in lines[0].split(",")]
        for line in lines[2:]:
            desired.append(line.strip())
    return patterns, desired


def part1(patterns, desired):
    @functools.lru_cache(maxsize=None)
    def combos(current):
        if current == "":
            return True
        return any(combos(current[len(p) :]) for p in patterns if current.startswith(p))

    return sum(combos(x) for x in desired)


def part2(patterns, desired):
    @functools.lru_cache(maxsize=None)
    def combos(current):
        if current == "":
            return 1
        return sum(combos(current[len(p) :]) for p in patterns if current.startswith(p))

    return sum(combos(x) for x in desired)


if __name__ == "__main__":
    print(part1(*parse_input("data/day19.txt")))
    print(part2(*parse_input("data/day19.txt")))
