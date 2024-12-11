# from cli import create_day_cli


def parse_input(path):
    fs_layout = []
    with open(path) as f:
        _id = 0
        for i, c in enumerate(f.read()):
            for k in range(int(c)):
                fs_layout.append(_id if i % 2 == 0 else ".")
            _id += 1 if i % 2 == 0 else 0
        return fs_layout


def part1(fs_layout):
    i = next(file_blocks(fs_layout))
    j, _ = next(free_blocks(fs_layout))
    while i > j:
        fs_layout[i], fs_layout[j] = fs_layout[j], fs_layout[i]
        i = next(file_blocks(fs_layout))
        j, _ = next(free_blocks(fs_layout))
    return checksum(fs_layout)


def part2(fs_layout):
    for i, file_size in files(fs_layout):
        for j, free_size in free_blocks(fs_layout):
            if j < i and free_size >= file_size:
                for k in range(file_size):
                    fs_layout[i + k], fs_layout[j + k] = (
                        fs_layout[j + k],
                        fs_layout[i + k],
                    )
                break
    return checksum(fs_layout)


def print_fs(fs_layout):
    print("".join(str(x) for x in fs_layout))


def checksum(fs_layout):
    return sum(i * fid for (i, fid) in enumerate(fs_layout) if fid != ".")


def files(fs_layout):
    i = len(fs_layout) - 1
    while i >= 0:
        if fs_layout[i] != ".":
            start = i
            while i >= 0 and fs_layout[i] == fs_layout[start]:
                i -= 1
            yield (i + 1, start - i)
        else:
            i -= 1


def file_blocks(fs_layout):
    for i, file_block in enumerate(reversed(fs_layout)):
        if file_block != ".":
            yield len(fs_layout) - 1 - i


def free_blocks(fs_layout):
    i = 0
    while i < len(fs_layout):
        if fs_layout[i] == ".":
            start = i
            while i < len(fs_layout) and fs_layout[i] == ".":
                i += 1
            yield (start, i - start)
        else:
            i += 1


# app = create_day_cli(day_number=9, input_parser=parse_input, part1=part1, part2=part2)

if __name__ == "__main__":
    # app()
    print(part1(parse_input("data/day9.txt")))
    print(part2(parse_input("data/day9.txt")))
