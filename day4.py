from collections import defaultdict

from cli import create_day_cli


def parse_input(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def part1(grid, word="XMAS"):
    directions = {
        "up": (-1, 0),
        "down": (+1, 0),
        "right": (0, +1),
        "left": (0, -1),
        "top_left": (-1, -1),
        "top_right": (-1, +1),
        "bottom_left": (+1, -1),
        "bottom_right": (+1, +1),
    }
    count = 0
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            count += (
                sum(dfs(grid, word, i, j, d, 0) for d in directions.values())
                if c == word[0]
                else 0
            )
    return count


def part2(grid, word="MAS"):
    directions = {
        "top_left": (-1, -1),
        "top_right": (-1, +1),
        "bottom_left": (+1, -1),
        "bottom_right": (+1, +1),
    }

    centers = defaultdict(int)
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c != word[0]:
                continue
            for d in directions.values():
                if dfs(grid, word, i, j, d, 0):
                    center = (i + d[0], j + d[1])
                    centers[center] += 1
    return len([x for x in centers.values() if x == 2])


def dfs(grid, word, i, j, direction, next_idx):
    if next_idx >= len(word):
        return True
    if not (0 <= i < len(grid) and 0 <= j < len(grid[i])):
        return False
    if grid[i][j] != word[next_idx]:
        return False
    return dfs(grid, word, i + direction[0], j + direction[1], direction, next_idx + 1)


app = create_day_cli(day_number=4, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    app()
