from PuzzleInput import ReadInput
from collections import defaultdict
import numpy as np

pz_input = [int(x) for x in ReadInput(13).data[0].split(",")]


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
    comp = Intcode(pz_input.copy())
    output = comp.run(0)
    data = []
    screen = {}
    while output is not None:
        data.append(output)
        if len(data) == 3:
            screen[(data[1], data[0])] = data[2]
            data = []
        output = comp.run(0)
    return len([x for x in screen if screen[x] == 2])


def part_b():
    np.set_printoptions(edgeitems=30, linewidth=100000)
    comp = Intcode(pz_input.copy())
    data = []
    screen = {}
    score = 0
    output = comp.run(0)
    while output is not None:
        data.append(output)
        if len(data) == 3:
            screen[(data[1], data[0])] = data[2]
            data = []
        output = comp.run(0)
    game = np.chararray((max([x[0] for x in screen])+1, max([y[1] for y in screen])+1))
    game[:] = "."
    ball_loc = (-1, -1)
    paddle_loc = (-1, -1)
    for item in screen:
        if screen[item] == 0:
            continue
        elif screen[item] == 1:
            game[item[0], item[1]] = "#"
        elif screen[item] == 2:
            game[item[0], item[1]] = "+"
        elif screen[item] == 3:
            game[item[0], item[1]] = "T"
            paddle_loc = (item[0], item[1])
        elif screen[item] == 4:
            game[item[0], item[1]] = "O"
            ball_loc = (item[0], item[1])
    comp.logic[0] = 2
    comp.reset()
    output = comp.run(0)
    data = []
    next_steer = 0
    while output is not None:
        data.append(output)
        if len(data) == 3:
            if data[0] == -1:
                score = data[2]
            else:
                game[data[1], data[0]] = "." if data[2] == 0 else "#" if data[2] == 1 else "+" if data[2] == 2 else "T" if data[2] == 3 else "O"
                if data[2] == 4:
                    ball_delta = (data[1] - ball_loc[0], data[0] - ball_loc[1])
                    if ball_delta[0] > 0:
                        next_steer = 1 if ((paddle_loc[0] - ball_loc[0] - 1) * ball_delta[1]) + ball_loc[1] > paddle_loc[1] else 0 if ((paddle_loc[0] - ball_loc[0] - 1) * ball_delta[1]) + ball_loc[1] == paddle_loc[1] else -1
                    else:
                        next_steer = 1 if paddle_loc[1] <= ball_loc[1] and ball_delta[1] > 0 else -1
                    ball_loc = (data[1], data[0])
                    # print("\n".join([row.tostring().decode("utf-8") for row in game]).replace(".", " "))
                elif data[2] == 3:
                    paddle_loc = (data[1], data[0])
            data = []
        output = comp.run(next_steer)
    return score


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
