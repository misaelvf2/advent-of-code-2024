from collections import defaultdict, deque

from cli import create_day_cli


def parse_input(path):
    rules = defaultdict(list)
    updates = []
    with open(path) as f:
        reading_rules = True
        for line in f:
            if line.isspace():
                reading_rules = False
                continue
            if reading_rules:
                before, after = line.split("|")
                rules[int(before)].append(int(after))
            else:
                updates.append([int(x) for x in line.split(",")])
    return rules, updates


def part1(rules, updates):
    result = 0
    for update in updates:
        result += update[len(update) // 2] if valid_update(rules, update) else 0
    return result


def part2(rules, updates):
    result = 0
    for update in updates:
        if not valid_update(rules, update):
            fixed = topological_sort(build_dependency_graph(rules, update))
            result += fixed[len(fixed) // 2] if fixed else 0
    return result


def valid_update(rules, update):
    seen = set()
    for page in update:
        if any([x in seen for x in rules[page]]):
            return False
        seen.add(page)
    return True


def build_dependency_graph(rules, update):
    graph = defaultdict(list)
    for page in update:
        for comes_after in rules[page]:
            if comes_after in set(update):
                graph[page].append(comes_after)
                if comes_after not in graph:
                    # Need to explicitly add nodes with no predecessors
                    # for Kahn's algorithm to work.
                    graph[comes_after] = []
    return graph


def topological_sort(graph):
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    sorted_order = []
    queue = deque([u for u in in_degree if in_degree[u] == 0])
    while queue:
        u = queue.popleft()
        sorted_order.append(u)

        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(sorted_order) == len(graph):
        return sorted_order
    return None


app = create_day_cli(day_number=5, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    app()
