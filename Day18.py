from PuzzleInput import ReadInput

pz_input = [list(x) for x in ReadInput(18).data]


class Pathfinder:
    def __init__(self, map, x, y, locations, inventory, dist):
        self.map = map
        self.x = x
        self.y = y
        self.locations = locations
        self.inventory = inventory
        self.distance_travelled = dist

    def copy(self):
        new_path = Pathfinder(self.map.copy(), self.x, self.y, self.locations, self.inventory.copy(), self.distance_travelled)
        return new_path

    def path_to(self, key):
        # A* to key
        # track any extra keys along the way
        # block on doors that are not in inventory
        # Once found, add dist to distance_travelled
        # update location
        pass


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
    test = True


def part_b():
    pass


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())

