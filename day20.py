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
    # Perform an initial DFS, storing the time it takes to get from each coordinate
    # to the end position. Do not use any cheats yet.
    # Then, look for all the valid cheat positions, and compute the saved time
    # using the previously-computed times as a range query.
    completion_times = {}
    seen = set()

    baseline = 0
    current = start
    while current is not None and current != end:
        seen.add(current)
        current = next_move(current, racetrack, seen)
        baseline += 1

    seen = set()
    current = start
    i = 0
    while current is not None and current != end:
        completion_times[current] = baseline - i
        seen.add(current)
        current = next_move(current, racetrack, seen)
        i += 1

    completion_times[end] = 0

    cheat_savings = defaultdict(int)
    seen = set()
    best_cheat = (float("-inf"), None)
    for current in completion_times.keys():
        if current not in seen:
            seen.add(current)
            for start, end in valid_cheats(current, racetrack, seen):
                saved = completion_times[current] - completion_times[end] - 2
                if saved > 0:
                    print(f"Saved {saved} picoseconds by taking cheat ({start}, {end})")
                    cheat_savings[saved] += 1
                    best_cheat = max(best_cheat, (saved, (start, end)))
                    # visualize(racetrack, (start, end))

    print(f"{baseline=}")
    print(f"Best cheat: {best_cheat[1]}, saving {best_cheat[0]} picoseconds")
    visualize(racetrack, (best_cheat[1][0], best_cheat[1][1]))
    return sum(v for k, v in cheat_savings.items() if k >= 100)


def part2(racetrack: list[list[str]], start: Point, end: Point, savings: int = 100):
    pass


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


def valid_cheats(current: Point, racetrack: list[list[str]], seen: set):
    def valid(p: Point, cheat_start: bool):
        if cheat_start:
            return (
                p not in seen
                and (0 <= p.x < len(racetrack[0]))
                and (0 <= p.y < len(racetrack))
                and (racetrack[p.y][p.x] == "#")
            )
        else:
            return (
                p not in seen
                and (0 <= p.x < len(racetrack[0]))
                and (0 <= p.y < len(racetrack))
                and (racetrack[p.y][p.x] != "#")
            )

    for direction in Direction:
        cheat_start = move(current, direction)
        cheat_end = move(cheat_start, direction)
        if valid(cheat_start, cheat_start=True) and valid(cheat_end, cheat_start=False):
            yield (cheat_start, cheat_end)


def next_move(current: Point, racetrack: list[list[str]], seen: set[Point]):
    def valid(p: Point):
        return (
            p not in seen
            and (0 <= p.x < len(racetrack[0]))
            and (0 <= p.y < len(racetrack))
            and (racetrack[p.y][p.x] != "#")
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
    print(part1(*parse_input("data/day20.txt")))
    print(part2(*parse_input("data/day20.txt")))
