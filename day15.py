import collections
from pprint import pprint

Point = collections.namedtuple("Point", ["x", "y"])


def parse_input(path):
    start = None
    grid, movements = [], []
    with open(path) as f:
        lines = [line.strip() for line in f.readlines()]
        i = 0
        while lines[i] != "":
            grid.append([c for c in lines[i]])
            find_start = lines[i].find("@")
            if find_start != -1:
                start = Point(x=find_start, y=i)
            i += 1
        i += 1
        movements = "".join(line for line in lines[i:])
    return grid, movements, start


def part1(grid, movements, start):
    current = start
    # draw_grid(grid)
    for movement in movements:
        next_position = try_move(grid, current, movement)
        grid[current.y][current.x] = "."
        grid[next_position.y][next_position.x] = "@"
        current = next_position
        # draw_grid(grid, movement)

    result = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "O":
                result += gps_coordinate(Point(x=j, y=i))

    return result


def part2(grid, movements, start):
    widened_grid, new_start = widen(grid)

    # draw_grid(widened_grid)
    current = new_start
    for i, movement in enumerate(movements):
        # draw_grid(widened_grid, movement)
        next_position = try_move_wide(widened_grid, current, movement)
        widened_grid[current.y][current.x] = "."
        widened_grid[next_position.y][next_position.x] = "@"
        current = next_position

    result = 0
    for i, row in enumerate(widened_grid):
        for j, c in enumerate(row):
            if c == "[":
                result += gps_coordinate(Point(x=j, y=i))

    return result


def widen(grid):
    new_start = None
    widened_grid = []
    for i, row in enumerate(grid):
        widened_row = []
        for j, c in enumerate(row):
            if c == "#":
                widened_row.append("#")
                widened_row.append("#")
            elif c == "O":
                widened_row.append("[")
                widened_row.append("]")
            elif c == ".":
                widened_row.append(".")
                widened_row.append(".")
            elif c == "@":
                new_start = Point(x=len(widened_row), y=i)
                widened_row.append("@")
                widened_row.append(".")
        widened_grid.append(widened_row)
    assert new_start is not None
    return widened_grid, new_start


def try_move_wide(grid, current: Point, direction) -> Point:
    def try_push(p):
        # Find all contiguous boxes in the current direction of movement
        if direction in ("<", ">"):
            can_push, contiguous = find_contiguous_horizontal(grid, p, direction)
            if can_push:
                for box_half in reversed(contiguous):
                    pushed = move(box_half, direction)
                    grid[pushed.y][pushed.x] = grid[box_half.y][box_half.x]
                    grid[box_half.y][box_half.x] = "."
                return True
            else:
                return False
        else:
            can_push, contiguous = find_contiguous_vertical(grid, p, direction)
            if can_push:
                ordered_rows = list(contiguous.keys())
                ordered_rows.sort(reverse=direction == "v")
                for row in ordered_rows:
                    for box in contiguous[row]:
                        pushed = move(box, direction)
                        grid[pushed.y][pushed.x] = grid[box.y][box.x]
                        grid[box.y][box.x] = "."
                return True
            else:
                return False

    next_position = move(current, direction)
    running_into = grid[next_position.y][next_position.x]
    match running_into:
        # If empty space, move freely
        case ".":
            return next_position
        # If wall, don't move
        case "#":
            return current
        # If box, try to push boxes
        case "[":
            if try_push(next_position):
                return next_position
            return current
        # If box, try to push boxes
        case "]":
            # if try_push(Point(x=next_position.x - 1, y=next_position.y)):
            if try_push(next_position):
                return next_position
            return current
        case _:
            raise ValueError


def find_contiguous_horizontal(grid, current: Point, direction):
    contiguous = []
    while grid[current.y][current.x] in ("[", "]"):
        contiguous.append(current)
        current = move(current, direction)
    can_push = grid[current.y][current.x] == "."
    return (can_push, contiguous)


def find_contiguous_vertical(grid, current: Point, direction):
    contiguous = collections.defaultdict(set)

    def helper(p, indent) -> bool:
        if p in contiguous[p.y]:
            return True
        contiguous[p.y].add(p)
        # Check next position in direction of movement
        next_position = move(p, direction)
        running_into = grid[next_position.y][next_position.x]
        # Running into wall
        if running_into == "#":
            return False
        # Running into empty space
        elif running_into == ".":
            return True
        # Running into box; check for alignment
        else:
            if running_into == grid[p.y][p.x]:
                return helper(next_position, indent + 1)
            else:
                success = helper(next_position, indent + 1)
                if not success:
                    return False
                if running_into == "]":
                    return helper(
                        Point(x=next_position.x - 1, y=next_position.y), indent + 1
                    )
                else:
                    return helper(
                        Point(x=next_position.x + 1, y=next_position.y), indent + 1
                    )

    if grid[current.y][current.x] == "[":
        can_push = helper(current, indent=0) and helper(
            Point(x=current.x + 1, y=current.y), indent=0
        )
    else:
        can_push = helper(current, indent=0) and helper(
            Point(x=current.x - 1, y=current.y), indent=0
        )
    return (can_push, contiguous)


def try_move(grid, current: Point, direction) -> Point:
    def try_push(p):
        # Try to push boxes
        # Find the last contiguous box in the current direction of movement
        lined_up = []
        while grid[p.y][p.x] == "O":
            lined_up.append(p)
            p = move(p, direction)
        can_push = grid[p.y][p.x] == "."
        if can_push:
            for box in reversed(lined_up):
                pushed = move(box, direction)
                grid[pushed.y][pushed.x] = "O"
                grid[box.y][box.x] = "."
            return True
        return False

    next_position = move(current, direction)
    running_into = grid[next_position.y][next_position.x]
    match running_into:
        # If empty space, move freely
        case ".":
            return next_position
        # If wall, don't move
        case "#":
            return current
        # If box, try to push boxes
        case "O":
            if try_push(next_position):
                return next_position
            return current
        case _:
            raise ValueError


def move(current, direction):
    match direction:
        case "<":
            return Point(x=current.x - 1, y=current.y)
        case ">":
            return Point(x=current.x + 1, y=current.y)
        case "^":
            return Point(x=current.x, y=current.y - 1)
        case "v":
            return Point(x=current.x, y=current.y + 1)
        case _:
            raise ValueError


def gps_coordinate(box: Point) -> int:
    return box.x + 100 * box.y


def draw_grid(grid, movement=None):
    if movement is None:
        pprint("Initial state:")
    else:
        pprint(f"Move {movement}")
    for line in grid:
        pprint("".join(c for c in line))
    pprint("")


if __name__ == "__main__":
    # print(part1(*parse_input("data/day15.txt")))
    print(part2(*parse_input("data/day15.txt")))
