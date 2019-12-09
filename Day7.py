from PuzzleInput import ReadInput
from itertools import permutations

pz_input = ReadInput(7).data[0].split(",")


class Intcode:
    logic = []

    def __init__(self, logic):
        self.logic = logic
        self.working_copy = logic
        self.i = 0
        self.phase_set = False

    def reset(self):
        self.working_copy = self.logic.copy()
        self.i = 0
        self.phase_set = False

    def run(self, phase, input):
        a_input = self.working_copy
        while True:
            command = int(a_input[self.i])
            if command == 99:
                return -1
            if command % 10 == 1:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                val_1 = int(a_input[int(a_input[self.i + 1])]) if mode_1 == 0 else int(a_input[self.i + 1])
                val_2 = int(a_input[int(a_input[self.i + 2])]) if mode_2 == 0 else int(a_input[self.i + 2])
                loc = int(a_input[self.i + 3])
                a_input[loc] = val_1 + val_2
                self.i += 4
            elif command % 10 == 2:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                val_1 = int(a_input[int(a_input[self.i + 1])]) if mode_1 == 0 else int(a_input[self.i + 1])
                val_2 = int(a_input[int(a_input[self.i + 2])]) if mode_2 == 0 else int(a_input[self.i + 2])
                loc = int(a_input[self.i + 3])
                a_input[loc] = val_1 * val_2
                self.i += 4
            elif command % 10 == 3:
                a_input[int(a_input[self.i + 1])] = phase if not self.phase_set else input
                self.phase_set = True
                self.i += 2
            elif command % 10 == 4:
                mode = (command // 100) % 10
                to_output = int(a_input[int(a_input[self.i + 1])]) if mode == 0 else int(a_input[self.i + 1])
                self.i += 2
                return to_output
            elif command % 10 == 5:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                if (mode_1 == 0 and int(a_input[int(a_input[self.i + 1])]) != 0) or (mode_1 == 1 and int(a_input[self.i + 1]) != 0):
                    self.i = int(a_input[int(a_input[self.i + 2])]) if mode_2 == 0 else int(a_input[self.i + 2])
                    continue
                self.i += 3
            elif command % 10 == 6:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                if (mode_1 == 0 and int(a_input[int(a_input[self.i + 1])]) == 0) or (mode_1 == 1 and int(a_input[self.i + 1]) == 0):
                    self.i = int(a_input[int(a_input[self.i + 2])]) if mode_2 == 0 else int(a_input[self.i + 2])
                    continue
                self.i += 3
            elif command % 10 == 7:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = (command // 10000) % 10
                val_1 = int(a_input[int(a_input[self.i + 1])]) if mode_1 == 0 else int(a_input[self.i + 1])
                val_2 = int(a_input[int(a_input[self.i + 2])]) if mode_2 == 0 else int(a_input[self.i + 2])
                loc = int(a_input[self.i + 3])
                a_input[loc] = 1 if val_1 < val_2 else 0
                self.i += 4
            elif command % 10 == 8:
                mode_1 = (command // 100) % 10
                mode_2 = (command // 1000) % 10
                mode_3 = (command // 10000) % 10
                val_1 = int(a_input[int(a_input[self.i + 1])]) if mode_1 == 0 else int(a_input[self.i + 1])
                val_2 = int(a_input[int(a_input[self.i + 2])]) if mode_2 == 0 else int(a_input[self.i + 2])
                loc = int(a_input[self.i + 3])
                a_input[loc] = 1 if val_1 == val_2 else 0
                self.i += 4
            else:
                raise AssertionError("Bad command %s" % command)


def part_a():
    comps = [Intcode(pz_input.copy()), Intcode(pz_input.copy()), Intcode(pz_input.copy()), Intcode(pz_input.copy()), Intcode(pz_input.copy())]
    options = list(permutations(range(5)))
    max_output = 0
    for option in options:
        comps[0].reset()
        comps[1].reset()
        comps[2].reset()
        comps[3].reset()
        comps[4].reset()
        output = comps[4].run(option[4], comps[3].run(option[3], comps[2].run(option[2], comps[1].run(option[1], comps[0].run(option[0], 0)))))
        if output > 0:
            max_output = max(max_output, output)
    return max_output


def part_b():
    comps = [Intcode(pz_input.copy()), Intcode(pz_input.copy()), Intcode(pz_input.copy()), Intcode(pz_input.copy()),
             Intcode(pz_input.copy())]
    options = list(permutations(range(5, 10)))
    max_output = 0
    for option in options:
        comps[0].reset()
        comps[1].reset()
        comps[2].reset()
        comps[3].reset()
        comps[4].reset()
        input = 0
        last_output = 0
        while True:
            last_output = input
            output_0 = comps[0].run(option[0], input)
            output_1 = comps[1].run(option[1], output_0)
            output_2 = comps[2].run(option[2], output_1)
            output_3 = comps[3].run(option[3], output_2)
            input = comps[4].run(option[4], output_3)
            if output_0 == -1 or output_1 == -1 or output_2 == -1 or output_3 == -1 or input == -1:
                break
        max_output = max(max_output, last_output)
    return max_output


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
