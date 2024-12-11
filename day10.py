# from cli import create_day_cli

DIRECTIONS = [(0, -1), (-1, 0), (+1, 0), (0, +1)]


def parse_input(path):
    top_map = []
    with open(path) as f:
        for line in f:
            top_map.append([])
            for c in line.strip():
                try:
                    top_map[-1].append(int(c))
                except ValueError:
                    top_map[-1].append(10)
    return top_map


def part1(top_map):
    result = 0
    reachable = {}

    def dfs(i, j):
        if top_map[i][j] == 9:
            return {(i, j)}
        if (i, j) in reachable:
            return reachable[(i, j)]
        reached = set()
        for d in DIRECTIONS:
            next_i, next_j = i + d[0], j + d[1]
            if gradually_uphill(i, j, next_i, next_j, top_map):
                reached.update(dfs(next_i, next_j))
        reachable[(i, j)] = reached
        return reached

    for i, line in enumerate(top_map):
        for j, height in enumerate(line):
            if height == 0:
                score = len(dfs(i, j))
                result += score

    return result


def within_bounds(i, j, n, m):
    return 0 <= i < n and 0 <= j < m


def gradually_uphill(i, j, p, q, top_map):
    n, m = len(top_map), len(top_map[0])
    if within_bounds(i, j, n, m) and within_bounds(p, q, n, m):
        return top_map[p][q] - top_map[i][j] == 1
    return False


def part2(top_map):
    result = 0
    reachable = {}

    def dfs(i, j):
        if top_map[i][j] == 9:
            return 1
        if (i, j) in reachable:
            return reachable[(i, j)]
        rating = 0
        for d in DIRECTIONS:
            next_i, next_j = i + d[0], j + d[1]
            if gradually_uphill(i, j, next_i, next_j, top_map):
                rating += dfs(next_i, next_j)
        reachable[(i, j)] = rating
        return rating

    for i, line in enumerate(top_map):
        for j, height in enumerate(line):
            if height == 0:
                rating = dfs(i, j)
                result += rating

    return result


# app = create_day_cli(day_number=1, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(parse_input("data/day10.txt")))
    print(part2(parse_input("data/day10.txt")))
