from collections import deque, namedtuple
from enum import StrEnum, auto

Point = namedtuple("Point", ["x", "y"])


class Direction(StrEnum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


def parse_input(path):
    return [tuple(map(int, line.split(","))) for line in open(path).readlines()]


def part1(coordinates: list[tuple[int, int]], bytes: int = 1024):
    memory_space = create_memory_space(coordinates, bytes=bytes)
    start = Point(0, 0)
    goal = Point(70, 70)

    seen = set()
    queue = deque([(start, 0)])
    while queue:
        current, steps = queue.popleft()
        if current in seen:
            continue
        if current == goal:
            return steps
        seen.add(current)
        for neighbor in neighbors(memory_space, current):
            queue.append((neighbor, steps + 1))

    return None


def part2(coordinates: list[tuple[int, int]]):
    low, high = 0, len(coordinates)
    while low < high:
        mid = (high + low) // 2
        print(low, mid, high)
        too_low = True if part1(coordinates, bytes=mid) is not None else False
        if too_low:
            low = mid + 1
        else:
            high = mid - 1

    return coordinates[low - 1]


def create_memory_space(coordinates, bytes):
    memory_space = [["." for _ in range(71)] for _ in range(71)]

    for byte in range(bytes):
        x, y = coordinates[byte]
        memory_space[y][x] = "#"

    return memory_space


def draw_memory_space(memory_space):
    for i, row in enumerate(memory_space):
        print("".join(c for c in row))


def neighbors(grid, current: Point):
    def valid(point: Point):
        return (0 <= point.x < len(grid[0]) and 0 <= point.y < len(grid)) and grid[
            point.y
        ][point.x] != "#"

    for direction in Direction:
        next_point = translate(current, direction)
        if valid(next_point):
            yield next_point


def translate(current: Point, direction: Direction):
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
    # print(part1(parse_input("data/day18.txt")))
    print(part2(parse_input("data/day18.txt")))
