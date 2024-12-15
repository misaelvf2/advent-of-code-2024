from collections import defaultdict, namedtuple

Point = namedtuple("Point", ["x", "y"])


DIRECTIONS = {
    "up": (-1, 0),
    "down": (+1, 0),
    "right": (0, +1),
    "left": (0, -1),
}


def parse_input(path):
    with open(path) as f:
        return [[x for x in line.strip()] for line in f.readlines()]


def part1(garden_map):
    height, width = len(garden_map), len(garden_map[0])
    result = 0
    seen = set()

    def dfs(i, j):
        if (i, j) in seen:
            return 0, 0
        seen.add((i, j))
        area = 1
        perimeter = compute_perimeter(i, j, garden_map)
        for d in DIRECTIONS.values():
            next_i, next_j = i + d[0], j + d[1]
            if (
                within_bounds(next_i, next_j, height, width)
                and garden_map[next_i][next_j] == garden_map[i][j]
            ):
                sub_area, sub_perimeter = dfs(next_i, next_j)
                area += sub_area
                perimeter += sub_perimeter
        return area, perimeter

    for i, row in enumerate(garden_map):
        for j, c in enumerate(row):
            if (i, j) not in seen:
                area, perimeter = dfs(i, j)
                result += area * perimeter

    return result


def part2(garden_map):
    height, width = len(garden_map), len(garden_map[0])
    result = 0
    seen = set()

    def dfs(i, j):
        if (i, j) in seen:
            return 0
        seen.add((i, j))
        area = 1
        near_walls = compute_walls(i, j, garden_map)
        for k, v in near_walls.items():
            walls[k].extend(v)
        for d in DIRECTIONS.values():
            next_i, next_j = i + d[0], j + d[1]
            if (
                within_bounds(next_i, next_j, height, width)
                and garden_map[i][j] == garden_map[next_i][next_j]
            ):
                area += dfs(next_i, next_j)
        return area

    for i, row in enumerate(garden_map):
        for j, c in enumerate(row):
            if (i, j) not in seen:
                walls = defaultdict(list)
                area = dfs(i, j)
                sides = count_sides(walls)
                result += area * sum(sides)

    return result


def within_bounds(i, j, height, width):
    return 0 <= i < height and 0 <= j < width


def compute_perimeter(i, j, garden_map):
    height, width = len(garden_map), len(garden_map[0])
    result = 0
    for d in DIRECTIONS.values():
        next_i, next_j = i + d[0], j + d[1]
        if not within_bounds(next_i, next_j, height, width):
            result += 1
        else:
            if garden_map[next_i][next_j] != garden_map[i][j]:
                result += 1
    return result


def compute_walls(i, j, garden_map):
    height, width = len(garden_map), len(garden_map[0])
    walls = defaultdict(list)

    for k, v in DIRECTIONS.items():
        next_i, next_j = i + v[0], j + v[1]
        if (
            not within_bounds(next_i, next_j, height, width)
            or garden_map[i][j] != garden_map[next_i][next_j]
        ):
            walls[k].append(Point(next_j, next_i))
    return walls


def count_sides(walls):
    horizontals = verticals = 0
    for k, v in walls.items():
        if k in ("up", "down"):
            v.sort(key=lambda p: (p.y, p.x), reverse=True)
            merged = [[v.pop()]]
            while v:
                current = v.pop()
                if horizontally_adjacent(current, merged[-1][-1]):
                    merged[-1].append(current)
                else:
                    merged.append([current])
            horizontals += len(merged)
        elif k in ("left", "right"):
            v.sort(key=lambda p: (p.x, p.y), reverse=True)
            merged = [[v.pop()]]
            while v:
                current = v.pop()
                if vertically_adjacent(current, merged[-1][-1]):
                    merged[-1].append(current)
                else:
                    merged.append([current])
            verticals += len(merged)

    return horizontals, verticals


def horizontally_adjacent(a: Point, b: Point) -> bool:
    return a.y == b.y and abs(a.x - b.x) == 1


def vertically_adjacent(a: Point, b: Point) -> bool:
    return a.x == b.x and abs(a.y - b.y) == 1


if __name__ == "__main__":
    print(part1(parse_input("data/day12.txt")))
    print(part2(parse_input("data/day12.txt")))
