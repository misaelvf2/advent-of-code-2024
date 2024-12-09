from typing import Optional

# from cli import create_day_cli


class Node:
    def __init__(
        self,
        data: tuple[int, int] | tuple[int, str],
        next: Optional["Node"] = None,
        prev: Optional["Node"] = None,
    ):
        self.data = data
        self.next = next
        self.prev = prev


def parse_input(path):
    head = tail = current = None
    _id = 0
    with open(path) as f:
        for i, c in enumerate(f.read()):
            val = (0, ".")
            for k in range(int(c)):
                val = (i + k, _id) if i % 2 == 0 else (i, ".")
                if not current:
                    current = Node(val)
                    head = current
                else:
                    current.next = Node(val)
                    current.next.prev = current
                    current = current.next
            if val[1] == _id:
                _id += 1
    tail = current
    return head, tail


def part1(head, tail):
    # print_list(head, reverse=False)
    p, q = next(free_blocks(head)), next(occupied_blocks(tail))
    i, j = (
        head.data[0] if head else float("inf"),
        tail.data[0] if tail else float("-inf"),
    )
    while i < j:
        p.data, q.data = (
            (p.data[0], q.data[1]),
            (q.data[0], p.data[1]),
        )
        p, q = next(free_blocks(p)), next(occupied_blocks(q))
        i, j = p.data[0] if p else float("inf"), q.data[0] if q else float("-inf")
    return checksum(head)


def part2(*args, **kwargs):
    pass


def print_list(head: Optional[Node], reverse: bool = False):
    while head:
        print(head.data[1], end="")
        head = head.next if not reverse else head.prev
    print("")


def free_blocks(head: Optional[Node]):
    while True:
        if not head:
            break
        if head.data[1] == ".":
            yield head
        head = head.next


def occupied_blocks(tail: Optional[Node]):
    while True:
        if not tail:
            break
        if tail.data[1] != ".":
            yield tail
        tail = tail.prev


def checksum(head: Optional[Node]):
    result = 0
    idx = 0
    while head:
        _, val = head.data
        if isinstance(val, int):
            result += idx * val
        head = head.next
        idx += 1
    return result


# app = create_day_cli(day_number=7, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(*parse_input("data/day9.txt")))
    print(part2(*parse_input("data/day9.txt")))
