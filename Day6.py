from PuzzleInput import ReadInput
from collections import defaultdict

pz_input = ReadInput(6).data
# pz_input = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"]


def part_a():
    orbits = defaultdict(lambda: [None, None])
    for orbit in pz_input:
        if orbit == "":
            continue
        pieces = orbit.split(")")
        orbits[pieces[1]][0] = pieces[0]
        if pieces[0] == "COM":
            orbits[pieces[1]][1] = 1
    made_change = True
    while made_change:
        made_change = False
        for orbit in [x for x in orbits]:
            if orbits[orbit][1] is None and orbits[orbits[orbit][0]][1] is not None:
                made_change = True
                orbits[orbit][1] = orbits[orbits[orbit][0]][1] + 1
    num_orbits = sum([orbits[x][1] for x in orbits])
    return num_orbits


def part_b():
    orbits = defaultdict(lambda: [None, None])
    for orbit in pz_input:
        if orbit == "":
            continue
        pieces = orbit.split(")")
        orbits[pieces[1]][0] = pieces[0]
        if pieces[0] == "COM":
            orbits[pieces[1]][1] = 1
    made_change = True
    while made_change:
        made_change = False
        for orbit in [x for x in orbits]:
            if orbits[orbit][1] is None and orbits[orbits[orbit][0]][1] is not None:
                made_change = True
                orbits[orbit][1] = orbits[orbits[orbit][0]][1] + 1
    you_path = [orbits["YOU"][0]]
    while orbits[you_path[-1]][0] != "COM":
        you_path.append(orbits[you_path[-1]][0])
    san_path = [orbits["SAN"][0]]
    while orbits[san_path[-1]][0] != "COM":
        san_path.append(orbits[san_path[-1]][0])
    while you_path[-1] == san_path[-1]:
        you_path = you_path[:-1]
        san_path = san_path[:-1]
    transfers = len(you_path) + len(san_path)
    return transfers


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
