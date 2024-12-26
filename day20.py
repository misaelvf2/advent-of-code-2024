from collections import defaultdict, namedtuple
from enum import StrEnum, auto

Point = namedtuple("Point", ["x", "y"])


class Direction(StrEnum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


def parse_input(path):
    racetrack = []
    start, end = None, None
    with open(path) as f:
        for i, line in enumerate(f):
            racetrack.append([])
            for j, c in enumerate(line.strip()):
                racetrack[-1].append(c)
                if c == "S":
                    start = Point(x=j, y=i)
                if c == "E":
                    end = Point(x=j, y=i)
    return racetrack, start, end


def part1(racetrack: list[list[str]], start: Point, end: Point, savings: int = 100):
    pass


def part2(
    racetrack: list[list[str]], start: Point, end: Point, minimum_savings: int = 100
):
    completion_times = compute_completion_times(racetrack, start, end)

    time_saved = defaultdict(int)
    unique_cheats = set()
    visited = set()
    for position, _ in completion_times.items():
        for _, cheat_end, cheat_length in cheats(
            racetrack, completion_times.keys(), position, visited, maximum_depth=20
        ):
            if (position, cheat_end) in unique_cheats:
                continue
            unique_cheats.add((position, cheat_end))
            saved = (
                completion_times[position] - completion_times[cheat_end] - cheat_length
            )
            if saved > 0:
                time_saved[saved] += 1
    return sum([v for k, v in time_saved.items() if k >= minimum_savings])


def visualize(racetrack, cheat):
    start, end = cheat
    original_start = racetrack[start.y][start.x]
    original_end = racetrack[end.y][end.x]
    racetrack[start.y][start.x] = "1"
    racetrack[end.y][end.x] = "2"
    for row in racetrack:
        print("".join(c for c in row))
    racetrack[start.y][start.x] = original_start
    racetrack[end.y][end.x] = original_end


def cheats(racetrack, positions, current, visited, maximum_depth: int = 20):
    def valid_cheat_start(p):
        return (
            0 <= p.x < len(racetrack[0])
            and 0 <= p.y < len(racetrack)
            and racetrack[p.y][p.x] == "#"
        )

    def valid_cheat_end(p):
        return (
            p not in visited
            and 0 <= p.x < len(racetrack[0])
            and 0 <= p.y < len(racetrack)
            and racetrack[p.y][p.x] != "#"
        )

    for direction in Direction:
        cheat_start = move(current, direction)
        if valid_cheat_start(cheat_start):
            cheat_ends = [
                x
                for x in positions
                if manhattan_distance(current, x) <= maximum_depth
                and valid_cheat_end(x)
            ]
            for cheat_end in cheat_ends:
                yield (
                    cheat_start,
                    cheat_end,
                    manhattan_distance(current, cheat_end),
                )


def closest(current, end):
    positions = [move(current, direction) for direction in Direction]
    positions.sort(key=lambda x: manhattan_distance(x, end))
    for position in positions:
        yield position


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def compute_completion_times(racetrack, start, end):
    completion_times = {}
    previous, current = None, start
    i = 0
    while current != end:
        completion_times[current] = i
        previous, current = current, next_position(racetrack, current, previous)
        i += 1
    baseline = i
    completion_times[end] = baseline
    for position, steps in completion_times.items():
        completion_times[position] = baseline - steps
    return completion_times


def next_position(racetrack, current, previous):
    def valid(p):
        return (
            p != previous
            and 0 <= p.x < len(racetrack[0])
            and 0 <= p.y < len(racetrack)
            and racetrack[p.y][p.x] != "#"
        )

    for direction in Direction:
        ahead = move(current, direction)
        if valid(ahead):
            return ahead

    return None


def move(current: Point, direction: Direction):
    match direction:
        case Direction.UP:
            return Point(current.x, current.y - 1)
        case Direction.DOWN:
            return Point(current.x, current.y + 1)
        case Direction.LEFT:
            return Point(current.x - 1, current.y)
        case Direction.RIGHT:
            return Point(current.x + 1, current.y)


if __name__ == "__main__":
    # print(part1(*parse_input("data/day20.txt")))
    print(part2(*parse_input("data/day20.txt")))
