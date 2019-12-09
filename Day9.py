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

    def run(self, input):
        a_input = self.working_copy
        while True:
            command = a_input[self.i]
            if command == 99:
                return None
            if command % 10 == 1:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                val_1 = a_input[a_input[self.i + 1]] if mode_1 == 0 else a_input[self.i + 1] if mode_1 == 1 else a_input[self.relative_base + a_input[self.i + 1]]
                val_2 = a_input[a_input[self.i + 2]] if mode_2 == 0 else a_input[self.i + 2] if mode_2 == 1 else a_input[self.relative_base + a_input[self.i + 2]]
                loc = a_input[self.i + 3]
                a_input[loc] = val_1 + val_2
                self.i += 4
            elif command % 10 == 2:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                val_1 = a_input[a_input[self.i + 1]] if mode_1 == 0 else a_input[self.i + 1] if mode_1 == 1 else a_input[self.relative_base + a_input[self.i + 1]]
                val_2 = a_input[a_input[self.i + 2]] if mode_2 == 0 else a_input[self.i + 2] if mode_2 == 1 else a_input[self.relative_base + a_input[self.i + 2]]
                loc = a_input[self.i + 3]
                a_input[loc] = val_1 * val_2
                self.i += 4
            elif command % 10 == 3:
                mode = (command // 100) % 10
                if mode == 0:
                    a_input[a_input[self.i + 1]] = input
                else:
                    a_input[self.relative_base + a_input[self.i + 1]] = input
                self.i += 2
            elif command % 10 == 4:
                mode = (command // 100) % 10
                to_output = a_input[a_input[self.i + 1]] if mode == 0 else a_input[self.i + 1] if mode == 1 else a_input[self.relative_base + a_input[self.i + 1]]
                self.i += 2
                return to_output
            elif command % 10 == 5:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                if (mode_1 == 0 and a_input[a_input[self.i + 1]] != 0) or (mode_1 == 1 and a_input[self.i + 1] != 0):
                    self.i = a_input[a_input[self.i + 2]] if mode_2 == 0 else a_input[self.i + 2] if mode_2 == 1 else a_input[self.relative_base + a_input[self.i + 2]]
                    continue
                self.i += 3
            elif command % 10 == 6:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                if (mode_1 == 0 and a_input[a_input[self.i + 1]] == 0) or (mode_1 == 1 and a_input[self.i + 1] == 0):
                    self.i = a_input[a_input[self.i + 2]] if mode_2 == 0 else a_input[self.i + 2] if mode_2 == 1 else a_input[self.relative_base + a_input[self.i + 2]]
                    continue
                self.i += 3
            elif command % 10 == 7:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = (command // 10000) % 10
                val_1 = a_input[a_input[self.i + 1]] if mode_1 == 0 else a_input[self.i + 1] if mode_1 == 1 else a_input[self.relative_base + a_input[self.i + 1]]
                val_2 = a_input[a_input[self.i + 2]] if mode_2 == 0 else a_input[self.i + 2] if mode_2 == 1 else a_input[self.relative_base + a_input[self.i + 2]]
                loc = a_input[self.i + 3]
                a_input[loc] = 1 if val_1 < val_2 else 0
                self.i += 4
            elif command % 10 == 8:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = (command // 10000) % 10
                val_1 = a_input[a_input[self.i + 1]] if mode_1 == 0 else a_input[self.i + 1] if mode_1 == 1 else a_input[self.relative_base + a_input[self.i + 1]]
                val_2 = a_input[a_input[self.i + 2]] if mode_2 == 0 else a_input[self.i + 2] if mode_2 == 1 else a_input[self.relative_base + a_input[self.i + 2]]
                loc = a_input[self.i + 3]
                a_input[loc] = 1 if val_1 == val_2 else 0
                self.i += 4
            elif command % 10 == 9:
                mode = (command // 100) % 10
                self.relative_base += a_input[a_input[self.i + 1]] if mode == 0 else a_input[self.i + 1] if mode == 1 else a_input[self.relative_base + a_input[self.i + 1]]
                self.i += 2
            else:
                raise AssertionError("Bad command %s" % command)


def part_a():
    comp = Intcode(pz_input)
    output = comp.run(1)
    last_output = output
    while output is not None:
        print(output)
        last_output = output
        output = comp.run(1)
    return last_output


def part_b():
    pass


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
