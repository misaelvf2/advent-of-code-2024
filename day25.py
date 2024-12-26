import itertools
from pprint import pprint


def parse_input(path):
    height = None
    schematics = []
    with open(path) as f:
        i = 0
        lines = [line.strip() for line in f.readlines()]
        while i < len(lines):
            schematic = []
            while i < len(lines) and lines[i] != "":
                schematic.append([c for c in lines[i]])
                i += 1
            if schematic:
                schematics.append(schematic)
            if height is None:
                height = i - 1
            i += 1
    return schematics, height


def part1(schematics, height):
    def is_lock(x):
        return all(c == "#" for c in x[0])

    def is_key(x):
        return all(c == "." for c in x[0])

    locks, keys = [], []
    for schematic in schematics:
        if is_lock(schematic):
            locks.append(make_lock(schematic, height))
        elif is_key(schematic):
            keys.append(make_key(schematic, height))
        else:
            pprint(f"None of the above? {schematic}")

    pprint(locks)
    pprint(keys)
    return sum(fit(key, lock, height) for key, lock in itertools.product(locks, keys))


def part2(schematics, height):
    pass


def fit(key, lock, height):
    return all(k + l < height for k, l in zip(key, lock))


def make_lock(schematic, lock_height):
    return tuple(
        lock_column_height(schematic, lock_height, j) for j in range(len(schematic[0]))
    )


def make_key(schematic, key_height):
    return tuple(
        key_column_height(schematic, key_height, j) for j in range(len(schematic[0]))
    )


def lock_column_height(schematic, lock_height, j):
    height = 0
    i = 0
    while i < lock_height and schematic[i][j] != ".":
        height += 1
        i += 1
    return height - 1


def key_column_height(schematic, key_height, j):
    height = 0
    i = 0
    while i < key_height and schematic[i][j] != "#":
        height += 1
        i += 1
    return key_height - height


if __name__ == "__main__":
    print(part1(*parse_input("data/day25.txt")))
    print(part2(*parse_input("data/day25.txt")))
