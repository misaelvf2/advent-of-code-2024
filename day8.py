from collections import namedtuple
from itertools import combinations

# from cli import create_day_cli

Point = namedtuple("Point", ["x", "y"])
Slope = namedtuple("Slope", ["run", "rise"])


def parse_input(path):
    grid, antennas = [], []
    with open(path) as f:
        for i, line in enumerate(f.readlines()):
            grid.append([])
            for j, c in enumerate(line.strip()):
                grid[i].append(c)
                if c.isalnum():
                    antennas.append(Point(x=j, y=i))
    return grid, antennas


def part1(grid, antennas):
    antinodes = set()
    antenna_pairs = [
        (p1, p2)
        for (p1, p2) in combinations(antennas, 2)
        if grid[p1.y][p1.x] == grid[p2.y][p2.x]
    ]

    n, m = len(grid), len(grid[0])
    for pair in antenna_pairs:
        antinodes.update(
            {
                node
                for node in draw_line(*pair)
                if within_bounds(node, width=m, height=n)
            }
        )

    visualize(grid, antinodes)
    return len(antinodes)


def visualize(grid, antinodes):
    for j, i in antinodes:
        grid[i][j] = "#"
    for line in grid:
        print("".join(line), end="\n")
    print("")


def draw_line(a: Point, b: Point):
    # Add node at start of line
    # The two antennas are at the center of the line
    # Add node at end of line
    slope = compute_slope(a, b)
    run, rise = abs(slope.run), abs(slope.rise)
    match direction(slope):
        case "←":
            start_antinode = Point(x=a.x + run, y=a.y)
            end_antinode = Point(x=b.x - run, y=b.y)
        case "→":
            start_antinode = Point(x=a.x - run, y=a.y)
            end_antinode = Point(x=b.x + run, y=b.y)
        case "↑":
            start_antinode = Point(x=a.x, y=a.y + rise)
            end_antinode = Point(x=b.x, y=b.y - rise)
        case "↓":
            start_antinode = Point(x=a.x, y=a.y - rise)
            end_antinode = Point(x=b.x, y=b.y + rise)
        case "↗":
            start_antinode = Point(x=a.x - run, y=a.y + rise)
            end_antinode = Point(x=b.x + run, y=b.y - rise)
        case "↖":
            start_antinode = Point(x=a.x + run, y=a.y + rise)
            end_antinode = Point(x=b.x - run, y=b.y - rise)
        case "↘":
            start_antinode = Point(x=a.x - run, y=a.y - rise)
            end_antinode = Point(x=b.x + run, y=b.y + rise)
        case "↙":
            start_antinode = Point(x=a.x + run, y=a.y - rise)
            end_antinode = Point(x=b.x - run, y=b.y + rise)
        case _:
            return set()
    return {start_antinode, end_antinode}


def direction(slope: Slope):
    if slope.rise == 0 and slope.run < 0:
        return "←"
    elif slope.rise == 0 and slope.run > 0:
        return "→"
    elif slope.rise < 0 and slope.run == 0:
        return "↑"
    elif slope.rise > 0 and slope.run == 0:
        return "↓"
    elif slope.run > 0 and slope.rise < 0:
        return "↗"
    elif slope.run < 0 and slope.rise < 0:
        return "↖"
    elif slope.run > 0 and slope.rise > 0:
        return "↘"
    elif slope.run < 0 and slope.rise > 0:
        return "↙"


def part2(grid, antennas):
    pass


def compute_slope(start: Point, end: Point) -> Slope:
    result = Slope(run=end.x - start.x, rise=end.y - start.y)
    return result


def within_bounds(p: Point, width: int, height: int) -> bool:
    return 0 <= p.x < width and 0 <= p.y < height


# app = create_day_cli(day_number=7, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(*parse_input("data/day8.txt")))
    print(part2(*parse_input("data/day8.txt")))
