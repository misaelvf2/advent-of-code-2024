from functools import lru_cache

# from cli import create_day_cli


def parse_input(path):
    with open(path) as f:
        return [int(stone) for stone in f.read().split(" ")]


def part1(stones: list[int], blinks: int = 25):
    for i in range(blinks):
        new_stones = []
        for stone in stones:
            new_stones.extend(rules(stone))
        stones = new_stones
    return len(stones)


def part2(stones: list[int], blinks: int = 75):
    @lru_cache(maxsize=None)
    def dfs(stone, blink):
        if blink == blinks:
            return 1
        total = 0
        applied_rule = rules(stone)
        for stone in applied_rule:
            total += dfs(stone, blink + 1)
        return total

    return sum(dfs(stone, 0) for stone in stones)


@lru_cache(maxsize=None)
def rules(stone: int):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        digit_length = len(str(stone))
        return [
            int(str(stone)[: digit_length // 2]),
            int(str(stone)[digit_length // 2 :]),
        ]
    else:
        return [stone * 2024]


# app = create_day_cli(day_number=1, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(parse_input("data/day11.txt")))
    print(part2(parse_input("data/day11.txt")))
