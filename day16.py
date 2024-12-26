import math
from collections import namedtuple
from enum import StrEnum, auto

from utils import PriorityQueue

Position = namedtuple("Position", ["x", "y"])
State = namedtuple("State", ["position", "heading"])


class Heading(StrEnum):
    NORTH = auto()
    SOUTH = auto()
    WEST = auto()
    EAST = auto()


class Rotation(StrEnum):
    CLOCKWISE = auto()
    COUNTERCLOCKWISE = auto()


def parse_input(path):
    start = goal = None
    grid = []
    with open(path) as f:
        for i, line in enumerate(f):
            grid.append([])
            for j, c in enumerate(line.strip()):
                if c == "S":
                    start = Position(x=j, y=i)
                elif c == "E":
                    goal = Position(x=j, y=i)
                grid[-1].append(c)
    return grid, start, goal


def part1(grid: list[list[str]], start: Position, goal: Position):
    start_state = State(position=start, heading=Heading.EAST)
    distances, predecessors = dijkstra(grid, start_state)
    draw_grid(grid, start, goal, predecessors)
    return min(v for k, v in distances.items() if k[0] == goal)


def part2(grid: list[list[str]], start: Position, goal: Position):
    start_state = State(position=start, heading=Heading.EAST)
    distances, predecessors = dijkstra(grid, start_state)

    end_state = (math.inf, None)
    for k, v in distances.items():
        if k[0] == goal:
            end_state = min(end_state, (v, k), key=lambda x: x[0])

    seen = set()

    def helper(current):
        if current in seen or current.position == start:
            return
        seen.add(current)
        for predecessor in predecessors[current]:
            helper(predecessor)

    helper(end_state[1])
    seen.add(start_state)

    unique_positions = {x.position for x in seen}
    return len(unique_positions)


def draw_grid(grid, start, goal, predecessors):
    heading_map = {
        Heading.NORTH: "^",
        Heading.SOUTH: "v",
        Heading.WEST: "<",
        Heading.EAST: ">",
    }
    current = State(position=goal, heading=Heading.EAST)
    while current:
        grid[current.position.y][current.position.x] = heading_map[current.heading]
        current = predecessors[current]
    grid[start.y][start.x] = "S"
    grid[goal.y][goal.x] = "E"
    for line in grid:
        print("".join(c for c in line))


def translate(current: State):
    position, heading = current.position, current.heading
    match current.heading:
        case Heading.NORTH:
            return State(
                position=Position(position.x, position.y - 1),
                heading=heading,
            )
        case Heading.SOUTH:
            return State(
                position=Position(position.x, position.y + 1),
                heading=heading,
            )
        case Heading.WEST:
            return State(
                position=Position(position.x - 1, position.y),
                heading=heading,
            )
        case Heading.EAST:
            return State(
                position=Position(position.x + 1, position.y),
                heading=heading,
            )
        case _:
            return current


def rotate(current: State, rotation: Rotation) -> State:
    position, heading = current.position, current.heading
    match heading:
        case Heading.NORTH:
            new_heading = (
                Heading.EAST if rotation == Rotation.CLOCKWISE else Heading.WEST
            )
        case Heading.SOUTH:
            new_heading = (
                Heading.WEST if rotation == Rotation.CLOCKWISE else Heading.EAST
            )
        case Heading.WEST:
            new_heading = (
                Heading.NORTH if rotation == Rotation.CLOCKWISE else Heading.SOUTH
            )
        case Heading.EAST:
            new_heading = (
                Heading.SOUTH if rotation == Rotation.CLOCKWISE else Heading.NORTH
            )
        case _:
            new_heading = heading
    return State(position=position, heading=new_heading)


def dijkstra(grid: list[list[str]], source: State):
    distances = {}
    distances[source] = 0
    predecessors = {}
    predecessors[source] = []

    priority_queue = PriorityQueue()
    priority_queue.add_item(source, 0)

    while priority_queue.heap:
        _, current_item, _ = priority_queue.pop_item()
        for neighbor, weight in neighbors(grid, current_item):
            if neighbor not in distances:
                distances[neighbor] = math.inf
                predecessors[neighbor] = []
                priority_queue.add_item(neighbor, math.inf)
            alternative = distances[current_item] + weight
            if alternative < distances[neighbor]:
                distances[neighbor] = alternative
                predecessors[neighbor] = [current_item]
                priority_queue.decrease_priority(neighbor, alternative)
            elif alternative == distances[neighbor]:
                predecessors[neighbor].append(current_item)

    return distances, predecessors


def neighbors(grid: list[list[str]], current: State):
    # Look ahead
    ahead = translate(current)
    if grid[ahead.position.y][ahead.position.x] != "#":
        yield (ahead, 1)
    # Look clockwise
    # clockwise = translate(rotate(current, rotation=Rotation.CLOCKWISE))
    clockwise = rotate(current, rotation=Rotation.CLOCKWISE)
    if grid[clockwise.position.y][clockwise.position.x] != "#":
        yield (clockwise, 1000)
    # Look counter-clockwise
    # counter_clockwise = translate(rotate(current, rotation=Rotation.COUNTERCLOCKWISE))
    counter_clockwise = rotate(current, rotation=Rotation.COUNTERCLOCKWISE)
    if grid[counter_clockwise.position.y][counter_clockwise.position.x] != "#":
        yield (counter_clockwise, 1000)


if __name__ == "__main__":
    # print(part1(*parse_input("data/day16.txt")))
    print(part2(*parse_input("data/day16.txt")))
