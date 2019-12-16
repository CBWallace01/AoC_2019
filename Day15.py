from PuzzleInput import ReadInput
from collections import defaultdict
import numpy as np

pz_input = [int(x) for x in ReadInput(15).data[0].split(",")]


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

    def copy(self):
        return Intcode(self.working_copy.copy())

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
    frontier = [((0, 0), 0, Intcode(pz_input.copy()))]
    to_explore, curr_dist, curr_comp = frontier.pop(0)
    explored = [(0, 0)]
    while True:
        for i in range(1, 5):
            # 1: N, 2: S, 3: W, 4: E
            new_coord = (to_explore[0] + ((1 * (-1 if i == 3 else 1)) if i == 3 or i == 4 else 0), to_explore[1] + ((1 * (-1 if i == 2 else 1)) if i == 1 or i == 2 else 0))
            if new_coord in explored:
                continue
            else:
                explored.append(new_coord)
            new_comp = curr_comp.copy()
            status = new_comp.run(i)
            if status == 0:
                continue
            elif status == 1:
                frontier.append((new_coord, curr_dist + 1, new_comp))
            elif status == 2:
                return curr_dist + 1
        to_explore, curr_dist, curr_comp = frontier.pop(0)


def part_b():
    frontier = [((0, 0), 0, Intcode(pz_input.copy()))]
    to_explore, curr_dist, curr_comp = frontier.pop(0)
    explored = [(0, 0)]
    locations = {(0, 0): 0}
    try:
        while True:
            for i in range(1, 5):
                # 1: N, 2: S, 3: W, 4: E
                new_coord = (to_explore[0] + ((1 * (-1 if i == 3 else 1)) if i == 3 or i == 4 else 0),
                             to_explore[1] + ((1 * (-1 if i == 2 else 1)) if i == 1 or i == 2 else 0))
                if new_coord in explored:
                    continue
                else:
                    explored.append(new_coord)
                new_comp = curr_comp.copy()
                status = new_comp.run(i)
                if status == 0:
                    locations[new_coord] = 0
                elif status == 1:
                    frontier.append((new_coord, curr_dist + 1, new_comp))
                    locations[new_coord] = 1
                elif status == 2:
                    locations[new_coord] = 2
            to_explore, curr_dist, curr_comp = frontier.pop(0)
    except IndexError:
        min_row = min(x[1] for x in locations)
        max_row = max(x[1] for x in locations)
        min_col = min(x[0] for x in locations)
        max_col = max(x[0] for x in locations)
        np.set_printoptions(edgeitems=max(max_row - min_row, max_col - min_col)+1, linewidth=100000)
        area = np.zeros(((max_row - min_row) + 1, (max_col - min_col) + 1))
        start = (-1, -1)
        for wall in [x for x in locations]:
            area[wall[1] - min_row, wall[0] - min_col] = locations[wall]
            if locations[wall] == 2:
                start = (wall[1] - min_row, wall[0] - min_col)
        # print(area)
        frontier = [(start, 0)]
        to_explore, curr_dist = frontier.pop(0)
        explored = [start]
        try:
            while True:
                for i in range(1, 5):
                    # 1: N, 2: S, 3: W, 4: E
                    new_coord = (to_explore[0] + ((1 * (-1 if i == 2 else 1)) if i == 1 or i == 2 else 0),
                                 to_explore[1] + ((1 * (-1 if i == 3 else 1)) if i == 3 or i == 4 else 0))
                    if new_coord in explored:
                        continue
                    else:
                        explored.append(new_coord)
                    status = area[new_coord[0], new_coord[1]]
                    if status == 1:
                        frontier.append((new_coord, curr_dist + 1))
                        locations[new_coord] = 1
                to_explore, curr_dist = frontier.pop(0)
        except IndexError:
            return curr_dist


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
