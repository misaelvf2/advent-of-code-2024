import math
import pprint
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
        # result = quadrant(position, (width, height))
        # pprint.pprint(f"{position} is in {result} quadrant")
        per_quadrant[quadrant(position, (width, height))].append(position)
    # draw_grid(positions, (width, height))
    return math.prod(len(v) for (k, v) in per_quadrant.items() if k != "middle")


def part2(robots: list[Robot]):
    pass


def translate(
    ticks: int,
    position: tuple[int, int],
    velocity: tuple[int, int],
    dimensions: tuple[int, int],
) -> tuple[int, int]:
    # final_x = (position[0] + velocity[0] * ticks) % dimensions[0]
    # final_y = (position[1] + velocity[1] * ticks) % dimensions[1]
    # pprint.pprint(f"{position} moving at {velocity} ends up at ({final_x}, {final_y})")
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
    grid = [["." for _ in range(dimensions[0])] for _ in range(dimensions[1])]

    for x, y in positions:
        grid[y][x] = "1" if grid[y][x] == "." else str(int(grid[y][x]) + 1)

    for row in grid:
        print("".join(c for c in row))


if __name__ == "__main__":
    print(part1(parse_input("data/day14.txt")))
    print(part2(parse_input("data/day14.txt")))
