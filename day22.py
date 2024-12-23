from collections import defaultdict, deque


def parse_input(path):
    with open(path) as f:
        return [int(x.strip()) for x in f.readlines()]


def part1(initial_secrets: list[int], iterations: int = 2000):
    result = 0
    for secret in initial_secrets:
        for _ in range(iterations):
            secret = generate_secret(secret)
        result += secret
    return result


def part2(initial_secrets: list[int], iterations: int = 2000, sequence_length: int = 4):
    sequence_prices = defaultdict(int)
    for secret in initial_secrets:
        seen = set()
        last_k = deque([], maxlen=sequence_length)
        for _ in range(iterations):
            secret, change = price_change(secret)
            last_k.append(change)
            if len(last_k) == sequence_length:
                k_gram = tuple(x for x in last_k)
                if k_gram not in seen:
                    sequence_prices[k_gram] += secret % 10
                    seen.add(k_gram)
    return max(sequence_prices.values())


def generate_secret(seed: int):
    def step1(x):
        return prune(mix(x, x * 64))

    def step2(x):
        return prune(mix(x, x // 32))

    def step3(x):
        return prune(mix(x, x * 2048))

    def mix(x, y):
        return x ^ y

    def prune(x):
        return x % 16777216

    return step3(step2(step1(seed)))


def price_change(seed: int):
    new_price = generate_secret(seed)
    return (new_price, new_price % 10 - seed % 10)


if __name__ == "__main__":
    print(part1(parse_input("data/day22.txt")))
    print(part2(parse_input("data/day22.txt")))
