from collections import deque
from enum import Enum, auto


class LogicalValue(Enum):
    TRUE = 1
    FALSE = 0
    INDETERMINATE = auto()


class LogicGate:
    def __init__(self, x, y, z, signals):
        self.x = x
        self.y = y
        self.z = z
        self.signals = signals

    def __repr__(self):
        return f"{self.x} {self.__class__.__name__} {self.y} = {self.z}"

    def process(self, event):
        if (
            event in (self.x, self.y)
            and self.signals[self.x] != LogicalValue.INDETERMINATE
            and self.signals[self.y] != LogicalValue.INDETERMINATE
        ):
            return self.emit()

    def __call__(self):
        raise NotImplementedError

    def emit(self):
        return (self.z, self())


class AND(LogicGate):
    def __call__(self):
        x, y = self.signals[self.x], self.signals[self.y]
        return x.value & y.value


class OR(LogicGate):
    def __call__(self):
        x, y = self.signals[self.x], self.signals[self.y]
        return x.value | y.value


class XOR(LogicGate):
    def __call__(self):
        x, y = self.signals[self.x], self.signals[self.y]
        return x.value ^ y.value


def parse_input(path):
    input_wires, gates, output_wires = {}, [], {}
    with open(path) as f:
        lines = [line.strip() for line in f]
        i = 0
        while lines[i] != "":
            wire, signal = lines[i].split(":")
            input_wires[wire] = LogicalValue(int(signal))
            i += 1
        i += 1
        while i < len(lines):
            inputs, output = lines[i].split("->")
            output = output.strip()
            x, operation, y = inputs.split()
            if output.startswith("z"):
                output_wires[output] = LogicalValue.INDETERMINATE
            else:
                input_wires[output] = LogicalValue.INDETERMINATE
            match operation:
                case "AND":
                    gates.append(AND(x, y, output, input_wires))
                case "OR":
                    gates.append(OR(x, y, output, input_wires))
                case "XOR":
                    gates.append(XOR(x, y, output, input_wires))
                case _:
                    raise ValueError(f"Unrecognized operation: {operation}")
            i += 1
    return input_wires, output_wires, gates


def part1(input_wires, output_wires, gates):
    event_queue = deque(
        (k, v) for k, v in input_wires.items() if v != LogicalValue.INDETERMINATE
    )

    while event_queue:
        wire, signal = event_queue.popleft()
        for gate in gates:
            emitted = gate.process(wire)
            if emitted is not None:
                event_queue.append(emitted)
                if emitted[0] in input_wires:
                    input_wires[emitted[0]] = LogicalValue(emitted[1])
        if wire in output_wires:
            output_wires[wire] = LogicalValue(signal)
        if wire in input_wires:
            input_wires[wire] = LogicalValue(signal)

    in_binary = binary_number(
        {
            k: v.value
            for k, v in output_wires.items()
            if k.startswith("z") and v != LogicalValue.INDETERMINATE
        }
    )
    in_decimal = int(in_binary, 2)
    return in_decimal


def part2(input_wires, output_wires, gates):
    pass


def binary_number(output_wires):
    sorted_keys = sorted(output_wires.keys(), reverse=True)
    return "".join(str(output_wires[k]) for k in sorted_keys)


if __name__ == "__main__":
    print(part1(*parse_input("data/day24.txt")))
    print(part2(*parse_input("data/day24.txt")))
