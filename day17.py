class Computer:
    def __init__(
        self, register_a: int, register_b: int, register_c: int, program: list[int]
    ):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.program = program
        self.instruction_pointer = 0
        self.output = []

    def execute(self) -> str:
        while self.instruction_pointer < len(self.program) - 1:
            self.decode(
                instruction=self.program[self.instruction_pointer],
                operand=self.program[self.instruction_pointer + 1],
            )
        return ",".join(str(x) for x in self.output)

    def decode(self, instruction, operand):
        match instruction:
            case 0:
                self.adv(operand)
            case 1:
                self.bxl(operand)
            case 2:
                self.bst(operand)
            case 3:
                self.jnz(operand)
            case 4:
                self.bxc(operand)
            case 5:
                self.out(operand)
            case 6:
                self.bdv(operand)
            case 7:
                self.cdv(operand)
            case _:
                return

    def combo(self, operand: int):
        if operand in list(range(4)):
            return operand
        elif operand == 4:
            return self.register_a
        elif operand == 5:
            return self.register_b
        elif operand == 6:
            return self.register_c
        else:
            raise ValueError

    def adv(self, operand: int):
        # print("adv")
        numerator = self.register_a
        denominator = 2 ** self.combo(operand)
        self.register_a = numerator // denominator
        self.instruction_pointer += 2

    def bxl(self, operand: int):
        self.register_b = self.register_b ^ operand
        self.instruction_pointer += 2

    def bst(self, operand: int):
        self.register_b = self.combo(operand) % 8
        self.instruction_pointer += 2

    def jnz(self, operand: int):
        if self.register_a == 0:
            self.instruction_pointer += 2
        else:
            self.instruction_pointer = operand

    def bxc(self, operand: int):
        self.register_b = self.register_b ^ self.register_c
        self.instruction_pointer += 2

    def out(self, operand: int):
        self.output.append(self.combo(operand) % 8)
        self.instruction_pointer += 2

    def bdv(self, operand: int):
        numerator = self.register_a
        denominator = 2 ** self.combo(operand)
        self.register_b = numerator // denominator
        self.instruction_pointer += 2

    def cdv(self, operand: int):
        numerator = self.register_a
        denominator = 2 ** self.combo(operand)
        self.register_c = numerator // denominator
        self.instruction_pointer += 2

    def __repr__(self) -> str:
        return f"Computer({self.register_a=}, {self.register_b=}, {self.register_c=}, {self.program=})"


def parse_input(path):
    with open(path) as f:
        lines = [line.strip() for line in f.readlines()]
        register_a = int(lines[0].split(":")[1].strip())
        register_b = int(lines[1].split(":")[1].strip())
        register_c = int(lines[2].split(":")[1].strip())
        program = [int(op) for op in lines[4].split(":")[1].strip().split(",")]
    return Computer(register_a, register_b, register_c, program)


def part1(computer: Computer):
    print(computer)
    result = computer.execute()
    print(result)


def part2():
    pass


if __name__ == "__main__":
    print(part1(parse_input("data/day17.txt")))
    # print(part2(*parse_input("data/day17.txt")))
