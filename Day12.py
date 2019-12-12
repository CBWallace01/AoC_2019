from PuzzleInput import ReadInput
import numpy as np

pz_input = ReadInput(12).data


class Moon:
    def __init__(self, x, y, z):
        self.location = np.array([x, y, z])
        self.initial_location = np.array([x, y, z])
        self.velocity = np.array([0, 0, 0])
        self.initial_velocity = np.array([0, 0, 0])
        self.diffs = np.array([0, 0, 0])

    def compare_with(self, moon):
        self.diffs += (moon.location > self.location).astype(int)
        self.diffs -= (moon.location < self.location).astype(int)

    def apply_diffs(self):
        self.velocity += self.diffs
        self.diffs = np.array([0, 0, 0])

    def move(self):
        self.location += self.velocity
        return np.array(np.logical_and(self.location == self.initial_location, self.velocity == self.initial_velocity))

    def calculate_energy(self):
        return np.absolute(self.location).sum() * np.absolute(self.velocity).sum()


def parse_moons(pz_in):
    moons = []
    for moon in pz_in:
        if moon == "":
            continue
        pieces = moon.split("=")
        moons.append(Moon(int(pieces[1][:-3]), int(pieces[2][:-3]), int(pieces[3][:-1])))
    return moons


def part_a():
    test = ["<x=-1, y=0, z=2>", "<x=2, y=-10, z=-7>", "<x=4, y=-8, z=8>", "<x=3, y=5, z=-1>"]
    moons = parse_moons(pz_input)
    for i in range(1000):
        for x in range(len(moons)):
            for y in range(len(moons)):
                if x == y:
                    continue
                moons[x].compare_with(moons[y])
        for moon in moons:
            moon.apply_diffs()
            moon.move()
    return sum([x.calculate_energy() for x in moons])


def part_b():
    test = ["<x=-1, y=0, z=2>", "<x=2, y=-10, z=-7>", "<x=4, y=-8, z=8>", "<x=3, y=5, z=-1>"]
    test2 = ["<x=-8, y=-10, z=0>", "<x=5, y=5, z=10>", "<x=2, y=-7, z=3>", "<x=9, y=-8, z=-3>"]
    moons = parse_moons(pz_input)
    i = 1
    pattern = [None, None, None]
    while True:
        for x in range(len(moons)):
            for y in range(len(moons)):
                if x == y:
                    continue
                moons[x].compare_with(moons[y])
        found_match = np.array([True, True, True])
        for moon in moons:
            moon.apply_diffs()
            found_match = np.array(np.logical_and(moon.move(), found_match))
        for j in range(3):
            if pattern[j] is None and found_match[j]:
                pattern[j] = i
        if None in pattern:
            i += 1
        else:
            return np.lcm.reduce(pattern, dtype=np.dtype("i8"))


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
