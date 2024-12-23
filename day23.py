import networkx as nx


def parse_input(path):
    graph = nx.Graph()
    with open(path) as f:
        for line in f:
            src, dst = line.strip().split("-")
            graph.add_edge(src, dst)
    return graph


def part1(graph):
    result = 0
    for clique in nx.enumerate_all_cliques(graph):
        if len(clique) == 3:
            result += any(x for x in clique if x.startswith("t"))
    return result


def part2(graph):
    cliques = nx.find_cliques(graph)
    maximal_clique = max(cliques, key=len)
    return ",".join(sorted(maximal_clique))


if __name__ == "__main__":
    print(part1(parse_input("data/day23.txt")))
    print(part2(parse_input("data/day23.txt")))
