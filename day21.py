from collections import defaultdict, deque

# import networkx as nx

DIRECTIONS = {
    # (+i, +j)
    "^": (-1, 0),
    "v": (+1, 0),
    "<": (0, -1),
    ">": (0, +1),
}


def parse_input(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def part1(codes: list[str]):
    def propagate(key):
        robot_1_key = robot_2_key = robot_3_key = None
        # User pushes key; robot_1 reacts
        # If user pushed "A", robot_1 pushes their current key
        if key == "A":
            robot_1_key = robot_1.current
        # otherwise, robot_1 moves their arm
        else:
            robot_1.move(key)
        # robot_1 pushes key; robot_2 reacts
        if robot_1_key is not None:
            # if robot_1 pushed "A", robot_2 pushes their current key
            if robot_1_key == "A":
                robot_2_key = robot_2.current
            # otherwise, robot_2 moves their arm
            else:
                robot_2.move(robot_1_key)
        # robot_2 pushes key; robot_2 reacts
        if robot_2_key is not None:
            # if robot_2 pushed "A", robot_3 pushes their current key
            if robot_2_key == "A":
                robot_3_key = robot_3.current
            # otherwise, robot_3 moves their arm
            else:
                robot_3.move(robot_2_key)
        return robot_3_key

    robot_1 = DirectionalKeypad()
    robot_2 = DirectionalKeypad()
    robot_3 = NumericKeypad()

    numeric_keypad_path_builder = bfs(
        robot_3._graph, [n for n in robot_3._graph.keys()]
    )
    directional_keypad_path_builder = bfs(
        robot_2._graph, [n for n in robot_2._graph.keys()]
    )

    # sequence = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    # print(
    #     path_to_presses(
    #         sequence, shortest_sequence_path(sequence, directional_keypad_path_builder)
    #     )
    # )

    result = 0
    for code in codes[:1]:
        robot_3_sequence = code
        robot_2_sequence = path_to_presses(
            robot_3_sequence,
            shortest_sequence_path(robot_3_sequence, numeric_keypad_path_builder),
        )
        robot_1_sequence = path_to_presses(
            robot_2_sequence,
            shortest_sequence_path(robot_2_sequence, directional_keypad_path_builder),
        )
        user_sequence = path_to_presses(
            robot_1_sequence,
            shortest_sequence_path(robot_1_sequence, directional_keypad_path_builder),
        )

        print(user_sequence)
        print(robot_1_sequence)
        print(robot_2_sequence)
        print(robot_3_sequence)
        result += complexity(code, len(user_sequence))

    return result


def part2(codes: list[str]):
    pass


def complexity(code, path_length):
    numeric = int("".join(x for x in code if x.isdigit()))
    print(f"{path_length} * {numeric}")
    return int("".join(x for x in code if x.isdigit())) * path_length


def path_to_presses(desired, path):
    result = []
    desired = deque(desired)
    path = deque(path)
    while desired:
        current = path.popleft()
        if current[1] == desired[0]:
            result.append("A")
            desired.popleft()
        result.append(current[0])
    return "".join(x for x in result if x is not None)


def shortest_sequence_path(sequence, pairwise, is_human: bool = False):
    result = []
    sequence = deque(sequence)
    if is_human:
        previous = sequence.popleft()
    else:
        previous = "A"
    while sequence:
        current = sequence.popleft()
        result.extend(pairwise((None, previous), (None, current)))
        previous = current
    return result


def bfs(graph, nodes):
    distances = defaultdict(dict)
    predecessors = defaultdict(dict)

    for start in nodes:
        distances[start][start] = 0
        predecessors[start][start] = None
        seen = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for direction, neighbor in graph[current].items():
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                distances[start][neighbor] = distances[start][current] + 1
                predecessors[start][neighbor] = (direction, current)
                queue.append(neighbor)

    def reconstruct_path(start, end):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[start[1]][current[1]]
        return path[::-1]

    return reconstruct_path


class NumericKeypad:
    def __init__(self):
        self._graph = self._build_graph()
        self.current = "A"

    def move(self, key):
        try:
            self.current = self._graph[self.current][key]
        except KeyError:
            raise RuntimeError("Panic!")

    def _build_graph(self):
        graph = defaultdict(dict)
        grid = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [None, "0", "A"],
        ]

        for i, row in enumerate(grid):
            for j, c in enumerate(row):
                for direction, change in DIRECTIONS.items():
                    if c is None:
                        continue
                    next_i, next_j = i + change[0], j + change[1]
                    if 0 <= next_i < len(grid) and 0 <= next_j < len(grid[0]):
                        neighbor = grid[next_i][next_j]
                        if neighbor is not None:
                            graph[c][direction] = neighbor
        return graph


class DirectionalKeypad:
    def __init__(self):
        self._graph = self._build_graph()
        self.current = "A"

    def move(self, key):
        try:
            self.current = self._graph[self.current][key]
        except KeyError:
            raise RuntimeError("Panic!")

    def _build_graph(self):
        graph = defaultdict(dict)
        grid = [
            [None, "^", "A"],
            ["<", "v", ">"],
        ]

        for i, row in enumerate(grid):
            for j, c in enumerate(row):
                for direction, change in DIRECTIONS.items():
                    if c is None:
                        continue
                    next_i, next_j = i + change[0], j + change[1]
                    if 0 <= next_i < len(grid) and 0 <= next_j < len(grid[0]):
                        neighbor = grid[next_i][next_j]
                        if neighbor is not None:
                            graph[c][direction] = neighbor
        return graph


if __name__ == "__main__":
    print(part1(parse_input("data/day21.txt")))
    print(part2(parse_input("data/day21.txt")))
