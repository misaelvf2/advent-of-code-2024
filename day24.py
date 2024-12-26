import random
from collections import defaultdict, deque, namedtuple
from enum import Enum, auto

Event = namedtuple("Event", ["wire", "value"])


class LogicalValue(Enum):
    TRUE = 1
    FALSE = 0
    INDETERMINATE = auto()


class Circuit:
    def __init__(self, wires, gates):
        self.wires = wires
        self.gates = gates

    def run(self):
        event_queue = deque(
            Event(wire=k, value=v) for k, v in self.wires["input"].items()
        )

        while event_queue:
            event = event_queue.popleft()
            if event.wire in self.wires["intermediate"]:
                self.wires["intermediate"][event.wire] = LogicalValue(event.value)
            if event.wire in self.wires["output"]:
                self.wires["output"][event.wire] = LogicalValue(event.value)
            for gate in self.gates:
                emitted = gate.process(event.wire)
                if emitted is not None:
                    event_queue.append(emitted)

    def _wire_value(self, wire):
        if wire in self.wires["input"]:
            return self.wires["input"][wire]
        elif wire in self.wires["intermediate"]:
            return self.wires["intermediate"][wire]
        else:
            raise ValueError("Invalid wire")

    def binary_number(self):
        sorted_keys = sorted(self.wires["output"].keys(), reverse=True)
        return "0b" + "".join(str(self.wires["output"][k].value) for k in sorted_keys)


class LogicGate:
    def __init__(self, x, y, z, circuit):
        self.x = x
        self.y = y
        self.z = z
        self.circuit = circuit

    def __repr__(self):
        return f"{self.x} {self.__class__.__name__} {self.y} = {self.z}"

    def process(self, wire):
        if (
            wire in (self.x, self.y)
            and self.circuit._wire_value(self.x) != LogicalValue.INDETERMINATE
            and self.circuit._wire_value(self.y) != LogicalValue.INDETERMINATE
        ):
            return self.emit()

    def emit(self):
        return Event(wire=self.z, value=self())

    def __call__(self):
        raise NotImplementedError


class AND(LogicGate):
    def __call__(self):
        x, y = self.circuit._wire_value(self.x), self.circuit._wire_value(self.y)
        return x.value & y.value


class OR(LogicGate):
    def __call__(self):
        x, y = self.circuit._wire_value(self.x), self.circuit._wire_value(self.y)
        return x.value | y.value


class XOR(LogicGate):
    def __call__(self):
        x, y = self.circuit._wire_value(self.x), self.circuit._wire_value(self.y)
        return x.value ^ y.value


output_to_gate_map = {}


def parse_input(path):
    wires = defaultdict(dict)
    gates = []
    circuit = Circuit(wires, gates)
    with open(path) as f:
        lines = [line.strip() for line in f]
        i = 0
        while lines[i] != "":
            wire, value = lines[i].split(":")
            wires["input"][wire] = LogicalValue(int(value))
            i += 1
        i += 1
        while i < len(lines):
            inputs, output = lines[i].split("->")
            output = output.strip()
            x, operation, y = inputs.split()
            if output.startswith("z"):
                wires["output"][output] = LogicalValue.INDETERMINATE
            else:
                wires["intermediate"][output] = LogicalValue.INDETERMINATE
            match operation:
                case "AND":
                    new_gate = AND(x, y, output, circuit)
                    gates.append(new_gate)
                    output_to_gate_map[output] = new_gate
                case "OR":
                    new_gate = OR(x, y, output, circuit)
                    gates.append(new_gate)
                    output_to_gate_map[output] = new_gate
                case "XOR":
                    new_gate = XOR(x, y, output, circuit)
                    gates.append(new_gate)
                    output_to_gate_map[output] = new_gate
                case _:
                    raise ValueError(f"Unrecognized operation: {operation}")
            i += 1
    return circuit


def part1(circuit: Circuit):
    circuit.run()
    in_binary = circuit.binary_number()
    in_decimal = int(in_binary, 2)
    return in_decimal


def part2(circuit: Circuit):
    bit_length = 45

    def set_positions(x):
        return [idx for idx, bit in enumerate(reversed(x)) if bit == "1"]

    maybe_bad_wires = set()
    for i in range(10):
        for j in range(10):
            x, y = random.randint(1, 34124143), random.randint(1, 34124143)
            manual_wires = input_as_decimal(x, y, bit_length)
            circuit.wires["input"].update(manual_wires)
            circuit.run()
            expected = bin(x + y)
            actual = circuit.binary_number()
            difference = bin(int(expected, 2) ^ int(actual, 2))
            print(f"Expected: {"0b" + expected[2:].zfill(bit_length)}", end=" ")
            print(f"Actual = {actual}", end=" ")
            print(f"Difference: {"0b" + difference[2:].zfill(bit_length)}", end=" ")
            print(f"Hamming distance: {int(difference[2:], 2).bit_count()}")
            maybe_bad_wires.update(find_bad_wires(circuit, actual, expected))

    always_good = (
        set(circuit.wires["output"].keys()) | set(circuit.wires["intermediate"].keys())
    ) - maybe_bad_wires
    print(always_good)


def find_bad_wires(circuit: Circuit, actual, expected):
    maybe_bad = set()

    def logic_func(gate):
        if isinstance(gate, AND):
            return lambda x, y: x & y
        if isinstance(gate, OR):
            return lambda x, y: x | y
        if isinstance(gate, XOR):
            return lambda x, y: x ^ y
        return lambda x, y: True

    def helper(gate, last_expected, depth):
        if gate() == last_expected:
            return depth
        maybe_bad.add(gate.z)
        store_x, store_y = (
            circuit._wire_value(gate.x).value,
            circuit._wire_value(gate.y).value,
        )
        # Try inverting x
        if logic_func(gate)(int(not store_x), store_y) == last_expected:
            if gate.x[0] not in ("x", "y"):
                return helper(output_to_gate_map[gate.x], int(not store_x), depth + 1)
        # Try inverting y
        elif logic_func(gate)(store_x, int(not store_y)) == last_expected:
            if gate.y[0] not in ("x", "y"):
                return helper(output_to_gate_map[gate.y], int(not store_y), depth + 1)
        # Try inverting both x and y
        elif logic_func(gate)(int(not store_x), int(not store_y)) == last_expected:
            if gate.x[0] not in ("x", "y"):
                return helper(output_to_gate_map[gate.x], int(not store_x), depth + 1)
            if gate.y[0] not in ("x", "y"):
                return helper(output_to_gate_map[gate.y], int(not store_y), depth + 1)

        return depth

    # Start from the z gates
    for wire, _ in [
        (wire, value)
        for wire, value in circuit.wires["output"].items()
        if wire.startswith("z")
    ]:
        position = int(wire[1:])
        if (int(actual, 2) >> position) & 1 != (int(expected, 2) & position) & 1:
            gate = output_to_gate_map[wire]
            maybe_bad.add(gate.z)
            max_depth = helper(gate, int(expected, 2) & position, 1)

    # print(max_depth)
    return maybe_bad


def input_as_decimal(x, y, bit_length):
    wires = {}
    for i in range(bit_length):
        wires[f"x0{i}"] = LogicalValue(x % 2)
        x //= 2
        wires[f"y0{i}"] = LogicalValue(y % 2)
        y //= 2
    return wires


def binary_number(output_wires):
    sorted_keys = sorted(output_wires.keys(), reverse=True)
    return "".join(str(output_wires[k]) for k in sorted_keys)


if __name__ == "__main__":
    print(part1(parse_input("data/day24.txt")))
    print(part2(parse_input("data/day24.txt")))
