from PuzzleInput import ReadInput
import numpy as np
from collections import defaultdict

pz_input = np.array([np.array(list(x)) for x in ReadInput(18).data])
# pz_input = np.array([list(x) for x in ["#########", "#b.A.@.a#", "#########"]])
# pz_input = np.array([list(x) for x in ["########################", "#f.D.E.e.C.b.A.@.a.B.c.#", "######################.#", "#d.....................#", "########################"]])
# pz_input = np.array([list(x) for x in ["#################", "#i.G..c...e..H.p#", "########.########", "#j.A..b...f..D.o#", "########@########", "#k.E..a...g..B.n#", "########.########", "#l.F..d...h..C.m#", "#################"]])


class Pathfinder:
    max_dist = float("Inf")

    def __init__(self, map, x, y, locations, inventory, dist):
        self.map = map
        self.row = x
        self.col = y
        self.locations = locations
        self.inventory = inventory
        self.distance_travelled = dist

    def copy(self):
        new_path = Pathfinder(self.map.copy(), self.row, self.col, self.locations, self.inventory.copy(), self.distance_travelled)
        return new_path

    def path_to(self, key):
        # A* to key
        # track any extra keys along the way
        # block on doors that are not in inventory
        # Once found, add dist to distance_travelled
        # update location
        explored = defaultdict(lambda: False)
        explored[(self.row, self.col)] = True
        paths = [(self.get_dist_to(key), (self.row, self.col), 0, self.inventory.copy())]
        _, curr_loc, curr_dist, curr_inv = paths.pop(0)
        while True:
            for i in range(4):
                new_loc = (curr_loc[0] + (1 * (1 if i == 3 else -1 if i == 1 else 0)), curr_loc[1] + (1 * (1 if i == 0 else -1 if i == 2 else 0)))
                if explored[new_loc] or self.map[new_loc[0]][new_loc[1]] == "#":
                    continue
                if ord(self.map[new_loc[0]][new_loc[1]]) in range(ord("A"), ord("Z")):
                    if chr(ord(self.map[new_loc[0]][new_loc[1]]) - (ord("A") - ord("a"))) not in curr_inv:
                        continue
                new_inv = curr_inv.copy()
                if ord(self.map[new_loc[0]][new_loc[1]]) in range(ord("a"), ord("z")) and self.map[new_loc[0]][new_loc[1]] not in new_inv:
                    new_inv.append(self.map[new_loc[0]][new_loc[1]])
                if ord(self.map[new_loc[0]][new_loc[1]]) in range(ord("a"), ord("z")) and self.map[new_loc[0]][new_loc[1]] == key:
                    self.row = new_loc[0]
                    self.col = new_loc[1]
                    self.distance_travelled += curr_dist + 1
                    self.inventory = new_inv.copy()
                    if len(self.get_remaining_keys()) == 0 and self.distance_travelled < Pathfinder.max_dist:
                        Pathfinder.max_dist = self.distance_travelled
                    return True
                new_dist = curr_dist + 1
                remaining = self.get_dist_to(key, new_loc)
                if self.distance_travelled + remaining + new_dist >= Pathfinder.max_dist:
                    continue
                explored[new_loc] = True
                paths.append((remaining + new_dist, new_loc, new_dist, new_inv))
            if len(paths) == 0:
                return False
            paths.sort(key=lambda x: x[0])
            _, curr_loc, curr_dist, curr_inv = paths.pop(0)

    def get_dist_to(self, key, curr=None):
        if curr is None:
            curr = (self.row, self.col)
        return abs(curr[0] - self.locations[key][0]) + abs(curr[1] - self.locations[key][1])

    def get_remaining_keys(self):
        return [x for x in self.locations if x not in self.inventory]


def find_best_path(pf):
    for key in pf.get_remaining_keys():
        new_child = pf.copy()
        made_it = new_child.path_to(key)
        if made_it:
            find_best_path(new_child)


def part_a():
    locations = {}
    start = (-1, -1)
    for row in range(len(pz_input)):
        for col in range(len(pz_input[row])):
            if ord(pz_input[row][col]) in range(ord("a"), ord("z")+1):
                locations[pz_input[row][col]] = (row, col)
            elif pz_input[row][col] == "@":
                start = (row, col)
    # create pathfinder for each key in locations
    # store in list
    # for each pathfinder in list, make copies for each key remaining to be found, run to those
    # e.g. for pf in pathfinders: work recursively from that one point through all combinations.
    # get minimum from first branch. prune any other branches that pass that min.
    # if new min is found, update score, and continue pruning
    # exhaustively search all possible combinations
    pf = Pathfinder(pz_input.copy(), start[0], start[1], locations, [], 0)
    find_best_path(pf)
    return Pathfinder.max_dist


def part_b():
    pass


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())

