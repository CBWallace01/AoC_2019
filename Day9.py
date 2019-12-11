from PuzzleInput import ReadInput
from collections import defaultdict

pz_input = ReadInput(9).data[0].split(",")


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
    # pz_input = [1102,34915192,34915192,7,4,7,99,0]
    comp = Intcode(pz_input)
    output = comp.run(1)
    last_output = output
    while output is not None:
        last_output = output
        output = comp.run(1)
    return last_output


def part_b():
    comp = Intcode(pz_input)
    output = comp.run(2)
    last_output = output
    while output is not None:
        last_output = output
        output = comp.run(2)
    return last_output


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
