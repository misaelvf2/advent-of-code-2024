# from cli import create_day_cli
DIRECTIONS = {
    "up": (-1, 0),
    "down": (+1, 0),
    "right": (0, +1),
    "left": (0, -1),
}


ORIENTATION_MAP = {
    "up": "right",
    "down": "left",
    "right": "down",
    "left": "up",
}


def parse_input(path):
    start = None
    patrol_map = []
    with open(path) as f:
        for i, line in enumerate(f.readlines()):
            patrol_map.append([x for x in line])
            for j, c in enumerate(line):
                if c == "^":
                    start = (i, j, "up")
    return start, patrol_map


def part1(start, patrol_map):
    n, m = len(patrol_map), len(patrol_map[0])
    visited = set()
    visited.add(start)

    def translate(direction):
        i, j, _ = start
        while True:
            next_i, next_j = i + DIRECTIONS[direction][0], j + DIRECTIONS[direction][1]
            if out_of_bounds(next_i, next_j, n, m):
                return
            if patrol_map[next_i][next_j] == "#":
                direction = ORIENTATION_MAP[direction]
            else:
                i, j = next_i, next_j
                visited.add((i, j))

    translate("up")
    return len(visited)


def out_of_bounds(i, j, height, width):
    return not (0 <= i < height and 0 <= j < width)


def part2(start, patrol_map):
    # Compute the original patrol path
    # For each node along the path, with the exception of the start node,
    # onwards. If the path forms a cycle, then we found a solution.
    solutions = set()
    original_path, _ = compute_path(start, patrol_map)

    prev_node = start
    for node in original_path:
        if node == start:
            continue
        i, j, _ = node
        temp = patrol_map[i][j]
        patrol_map[i][j] = "#"
        _, forms_cycle = compute_path(prev_node, patrol_map)
        if forms_cycle:
            solutions.add((i, j))
        patrol_map[i][j] = temp

    return len(solutions)


def compute_path(start, patrol_map):
    path = {start}
    i, j, heading = start
    n, m = len(patrol_map), len(patrol_map[0])
    while True:
        next_i, next_j = i + DIRECTIONS[heading][0], j + DIRECTIONS[heading][1]
        if out_of_bounds(next_i, next_j, n, m):
            return path, False
        if patrol_map[next_i][next_j] == "#":
            heading = ORIENTATION_MAP[heading]
            if (i, j, heading) in path:
                return path, True
            path.add((i, j, heading))
        else:
            if (next_i, next_j, heading) in path:
                return path, True
            path.add((next_i, next_j, heading))
            i, j = next_i, next_j


# app = create_day_cli(day_number=5, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(*parse_input("data/day6.txt")))
    print(part2(*parse_input("data/day6.txt")))
