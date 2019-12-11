from PuzzleInput import ReadInput
from collections import defaultdict
import numpy as np

pz_input = [int(x) for x in ReadInput(11).data[0].split(",")]


class Intcode:
    logic = []

    def __init__(self, logic):
        self.logic = defaultdict(lambda: 0)
        for i in range(len(logic)):
            self.logic[i] = int(logic[i])
        self.working_copy = self.logic.copy()
        self.i = 0
        self.relative_base = 0

    def reset(self):
        self.working_copy = self.logic.copy()
        self.i = 0

    def get_value(self, logic, mode, i):
        if mode == 0:
            return logic[logic[i]]
        elif mode == 1:
            return logic[i]
        elif mode == 2:
            return logic[self.relative_base + logic[i]]

    def run(self, input):
        a_input = self.working_copy
        while True:
            command = a_input[self.i]
            if command == 99:
                return None
            # Addition
            if command % 10 == 1:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = 2 if (command // 10000) % 10 == 2 else 0
                val_1 = self.get_value(a_input, mode_1, self.i + 1)
                val_2 = self.get_value(a_input, mode_2, self.i + 2)
                loc = self.relative_base + a_input[self.i + 3] if mode_3 == 2 else a_input[self.i + 3]
                a_input[loc] = val_1 + val_2
                self.i += 4
            # Multiplication
            elif command % 10 == 2:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = 2 if (command // 10000) % 10 == 2 else 0
                val_1 = self.get_value(a_input, mode_1, self.i + 1)
                val_2 = self.get_value(a_input, mode_2, self.i + 2)
                loc = self.relative_base + a_input[self.i + 3] if mode_3 == 2 else a_input[self.i + 3]
                a_input[loc] = val_1 * val_2
                self.i += 4
            # Input
            elif command % 10 == 3:
                mode = 2 if (command // 100) % 10 == 2 else 0
                if mode == 0:
                    a_input[a_input[self.i + 1]] = input
                elif mode == 2:
                    a_input[self.relative_base + a_input[self.i + 1]] = input
                self.i += 2
            # Output
            elif command % 10 == 4:
                mode = (command // 100) % 10
                to_output = self.get_value(a_input, mode, self.i + 1)
                self.i += 2
                return to_output
            # Jump if true (non-zero)
            elif command % 10 == 5:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                if self.get_value(a_input, mode_1, self.i + 1) != 0:
                    self.i = self.get_value(a_input, mode_2, self.i + 2)
                    continue
                self.i += 3
            # Jump if false (zero)
            elif command % 10 == 6:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                if self.get_value(a_input, mode_1, self.i + 1) == 0:
                    self.i = self.get_value(a_input, mode_2, self.i + 2)
                    continue
                self.i += 3
            # Less than
            elif command % 10 == 7:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = 2 if (command // 10000) % 10 == 2 else 0
                val_1 = self.get_value(a_input, mode_1, self.i + 1)
                val_2 = self.get_value(a_input, mode_2, self.i + 2)
                loc = self.relative_base + a_input[self.i + 3] if mode_3 == 2 else a_input[self.i + 3]
                a_input[loc] = 1 if val_1 < val_2 else 0
                self.i += 4
            # Equals
            elif command % 10 == 8:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = 2 if (command // 10000) % 10 == 2 else 0
                val_1 = self.get_value(a_input, mode_1, self.i + 1)
                val_2 = self.get_value(a_input, mode_2, self.i + 2)
                loc = self.relative_base + a_input[self.i + 3] if mode_3 == 2 else a_input[self.i + 3]
                a_input[loc] = 1 if val_1 == val_2 else 0
                self.i += 4
            # Relative base adjust
            elif command % 10 == 9:
                mode = (command // 100) % 10
                self.relative_base += self.get_value(a_input, mode, self.i + 1)
                self.i += 2
            else:
                raise AssertionError("Bad command %s" % command)


def part_a():
    x = 0
    y = 0
    direction = 0  # 0: up, 1: right, 2: down: 3: left
    colors = defaultdict(lambda: (0, 0))
    comp = Intcode(pz_input.copy())
    output = comp.run(colors[x, y][0])
    while output is not None:
        colors[(x, y)] = (output, colors[(x, y)][1] + (1 if output != colors[(x, y)][1] else 0))
        direction = (direction + (1 if comp.run(colors[x, y]) == 1 else -1)) % 4
        if direction % 2 == 0:
            y += 1 if direction == 0 else -1
        else:
            x += 1 if direction == 1 else -1
        output = comp.run(colors[x, y][0])
    return sum([1 for x in colors.values() if x[1] >= 1])


def part_b():
    x = 0
    y = 0
    direction = 0  # 0: up, 1: right, 2: down: 3: left
    colors = defaultdict(lambda: (0, 0))
    colors[(0, 0)] = (1, 0)
    comp = Intcode(pz_input.copy())
    output = comp.run(colors[x, y][0])
    while output is not None:
        colors[(x, y)] = (output, colors[(x, y)][1] + (1 if output != colors[(x, y)][1] else 0))
        direction = (direction + (1 if comp.run(colors[x, y]) == 1 else -1)) % 4
        if direction % 2 == 0:
            y += 1 if direction == 0 else -1
        else:
            x += 1 if direction == 1 else -1
        output = comp.run(colors[x, y][0])
    x_offset = min([x[0] for x in colors.keys()])
    y_offset = min([y[1] for y in colors.keys()])
    registration = np.zeros((max([y[1] for y in colors.keys()])-y_offset+1, max([x[0] for x in colors.keys()])-x_offset+1))
    for j in range(len(registration)):
        for i in range(len(registration[j])):
            registration[j, i] = colors[(i+x_offset, j+y_offset)][0]
    return registration



if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
