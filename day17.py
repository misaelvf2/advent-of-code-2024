import math

import matplotlib.pyplot as plt


class Computer:
    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_c: int,
        program: list[int],
        debugger: "Debugger",
    ):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.program = program
        self.instruction_pointer = 0
        self.output = []
        self.debugger = debugger

    def execute(self) -> str:
        while self.instruction_pointer < len(self.program) - 1:
            self.decode(
                instruction=self.program[self.instruction_pointer],
                operand=self.program[self.instruction_pointer + 1],
            )
        self.debugger.register_states.append(oct(self.register_a))
        return ",".join(str(x) for x in self.output)

    def decode(self, instruction, operand):
        self.debugger.instruction_pointer_states.append(self.instruction_pointer)
        match instruction:
            case 0:
                self.debugger.instructions.append("adv")
                self.adv(operand)
            case 1:
                self.debugger.instructions.append("bxl")
                self.bxl(operand)
            case 2:
                self.debugger.instructions.append("bst")
                self.bst(operand)
            case 3:
                self.debugger.instructions.append("jnz")
                self.jnz(operand)
            case 4:
                self.debugger.instructions.append("bxc")
                self.bxc(operand)
            case 5:
                self.debugger.instructions.append("out")
                self.out(operand)
            case 6:
                self.debugger.instructions.append("bdv")
                self.bdv(operand)
            case 7:
                self.debugger.instructions.append("cdv")
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
        self.debugger.register_states.append(oct(self.register_a))
        self.output.append(self.combo(operand) % 8)
        self.instruction_pointer += 2
        self.debugger.outputs.append(self.output[-1])

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

    def reset(self):
        self.register_a = 0
        self.register_b = 0
        self.register_c = 0
        self.instruction_pointer = 0
        self.output = []

    def __repr__(self) -> str:
        return f"Computer({self.register_a=}, {self.register_b=}, {self.register_c=}, {self.program=})"


class Debugger:
    def __init__(self, register_a, register_b, register_c, program):
        self.computer = Computer(
            register_a, register_b, register_c, program, debugger=self
        )
        self.instructions = []
        self.outputs = []
        self.register_states = []
        self.instruction_pointer_states = []

    def execute(self):
        self.computer.execute()

    def reset(self):
        self.computer.reset()
        self.instructions = []
        self.outputs = []
        self.register_states = []
        self.instruction_pointer_states = []


def parse_input(path):
    with open(path) as f:
        lines = [line.strip() for line in f.readlines()]
        register_a = int(lines[0].split(":")[1].strip())
        register_b = int(lines[1].split(":")[1].strip())
        register_c = int(lines[2].split(":")[1].strip())
        program = [int(op) for op in lines[4].split(":")[1].strip().split(",")]
    return Debugger(register_a, register_b, register_c, program)


def part1(computer: Computer):
    result = computer.execute()
    return result


def part2(debugger: Debugger):
    # for i in range(10000):
    for i in [0o3002, 0o403002, 0o23002, 0o33002, 0o43002, 0o63002, 0o103002]:
        debugger.computer.register_a = i
        debugger.execute()
        raw_output = ",".join(str(x) for x in debugger.outputs)
        if raw_output.startswith("2,4,1"):
            print(raw_output, debugger.register_states)
        # print(
        #     f"register_a (octal): {oct(i)}, output (octal): {oct(as_number(raw_output))}, output (raw): {raw_output}",
        # )
        debugger.reset()


def as_number(output):
    result = 0
    i = 0
    # for i, val in enumerate(reversed(output.split(","))):
    for i, val in enumerate(output.split(",")):
        result += math.pow(8, i) * int(val)
    return int(result)


def visualize(data):
    plt.figure(figsize=(8, 6))
    plt.plot(data, marker="o", linestyle="-", color="b")
    plt.title("Outputs")
    plt.xlabel("Iteration")
    plt.ylabel("Output")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    print(part1(parse_input("data/day17.txt")))
    print(part2(parse_input("data/day17.txt")))
