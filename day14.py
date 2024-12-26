import math
from collections import defaultdict, namedtuple

Robot = namedtuple("Robot", ["x_pos", "y_pos", "x_vel", "y_vel"])


def parse_input(path):
    robots = []
    with open(path) as f:
        for line in f:
            position, velocity = line.split(" ")
            x_pos, y_pos = position[2:].split(",")
            x_vel, y_vel = velocity[2:].split(",")
            robots.append(Robot(int(x_pos), int(y_pos), int(x_vel), int(y_vel)))
    return robots


def part1(robots: list[Robot], ticks: int = 100, width: int = 101, height: int = 103):
    positions = []
    for robot in robots:
        positions.append(
            translate(
                ticks,
                (robot.x_pos, robot.y_pos),
                (robot.x_vel, robot.y_vel),
                (width, height),
            )
        )
    per_quadrant = defaultdict(list)
    for position in positions:
        per_quadrant[quadrant(position, (width, height))].append(position)
    return math.prod(len(v) for (k, v) in per_quadrant.items() if k != "middle")


def part2(
    robots: list[Robot], ticks: int = 10_000, width: int = 101, height: int = 103
):
    positions = [
        (robot.x_pos, robot.y_pos, robot.x_vel, robot.y_vel) for robot in robots
    ]

    minimum_safety_factor = (math.inf, None)
    for i in range(ticks):
        for j, position in enumerate(positions):
            positions[j] = (
                *translate(
                    1,
                    (position[0], position[1]),
                    (position[2], position[3]),
                    (width, height),
                ),
                position[2],
                position[3],
            )

        per_quadrant = defaultdict(list)
        for position in positions:
            per_quadrant[quadrant((position[0], position[1]), (width, height))].append(
                position
            )

        minimum_safety_factor = min(
            minimum_safety_factor, (safety_factor(per_quadrant), i + 1)
        )
    return minimum_safety_factor


def safety_factor(robots_per_quadrant):
    return math.prod(len(v) for (k, v) in robots_per_quadrant.items() if k != "middle")


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def translate(
    ticks: int,
    position: tuple[int, int],
    velocity: tuple[int, int],
    dimensions: tuple[int, int],
) -> tuple[int, int]:
    return (
        (position[0] + velocity[0] * ticks) % dimensions[0],
        (position[1] + velocity[1] * ticks) % dimensions[1],
    )


def quadrant(position: tuple[int, int], dimensions: tuple[int, int]):
    if position[0] < dimensions[0] // 2 and position[1] < dimensions[1] // 2:
        return "top-left"
    elif position[0] < dimensions[0] // 2 and position[1] > dimensions[1] // 2:
        return "bottom-left"
    elif position[0] > dimensions[0] // 2 and position[1] > dimensions[1] // 2:
        return "bottom-right"
    elif position[0] > dimensions[0] // 2 and position[1] < dimensions[1] // 2:
        return "top-right"
    else:
        return "middle"


def draw_grid(positions: list[tuple[int, int]], dimensions: tuple[int, int]):
    grid = [[" " for _ in range(dimensions[0])] for _ in range(dimensions[1])]

    for x, y in positions:
        grid[y][x] = "X"

    print("\033c", end="")
    for row in grid:
        print("".join(c for c in row))


if __name__ == "__main__":
    print(part1(parse_input("data/day14.txt")))
    print(part2(parse_input("data/day14.txt")))
