from PuzzleInput import ReadInput
import time
import numpy as np
from collections import defaultdict
import collections

pz_input = np.array([np.array(list(x)) for x in ReadInput(18).data])
# pz_input = np.array([list(x) for x in ["#########", "#b.A.@.a#", "#########"]])
# pz_input = np.array([list(x) for x in ["########################", "#f.D.E.e.C.b.A.@.a.B.c.#", "######################.#", "#d.....................#", "########################"]])
# pz_input = np.array([list(x) for x in ["########################", "#...............b.C.D.f#", "#.######################", "#.....@.a.B.c.d.A.e.F.g#", "########################"]])
# pz_input = np.array([list(x) for x in ["#################", "#i.G..c...e..H.p#", "########.########", "#j.A..b...f..D.o#", "########@########", "#k.E..a...g..B.n#", "########.########", "#l.F..d...h..C.m#", "#################"]])
# pz_input = np.array([list(x) for x in ["########################", "#@..............ac.GI.b#", "###d#e#f################", "###A#B#C################", "###g#h#i################", "########################"]])


def find_best_path(pf):
    for key in pf.get_remaining_keys():
        new_child = pf.copy()
        made_it = new_child.path_to(key)
        if made_it:
            find_best_path(new_child)


def get_dist_to(curr, finish):
    return abs(curr[0] - finish[0]) + abs(curr[1] - finish[1])


def dist_between(start, finish, map):
    explored = defaultdict(lambda: False)
    explored[start] = True
    paths = [(get_dist_to(start, finish), start, 0, [], [])]
    _, curr_loc, curr_dist, curr_inv, curr_doors = paths.pop(0)
    while True:
        for i in range(4):
            new_loc = (curr_loc[0] + (1 * (1 if i == 3 else -1 if i == 1 else 0)), curr_loc[1] + (1 * (1 if i == 0 else -1 if i == 2 else 0)))
            if explored[new_loc] or map[new_loc[0]][new_loc[1]] == "#":
                continue
            new_doors = curr_doors.copy()
            if ord(map[new_loc[0]][new_loc[1]]) in range(ord("A"), ord("Z")):
                new_doors.append(map[new_loc[0]][new_loc[1]])
            new_inv = curr_inv.copy()
            if new_loc == finish:
                return curr_dist + 1, new_inv, new_doors
            if ord(map[new_loc[0]][new_loc[1]]) in range(ord("a"), ord("z")) and map[new_loc[0]][new_loc[1]] not in new_inv:
                new_inv.append(map[new_loc[0]][new_loc[1]])
            new_dist = curr_dist + 1
            remaining = get_dist_to(new_loc, finish)
            explored[new_loc] = True
            paths.append((remaining + new_dist, new_loc, new_dist, new_inv, new_doors))
        if len(paths) == 0:
            return None
        paths.sort(key=lambda x: x[0])
        _, curr_loc, curr_dist, curr_inv, curr_doors = paths.pop(0)


seen = {}
def min_path(curr_loc, inv, locations, distances):
    if (curr_loc, "".join(sorted(inv))) in seen:
        return seen[(curr_loc, "".join(sorted(inv)))]
    remaining_keys = [x for x in locations if x != "start" and x not in inv]
    if len(remaining_keys) == 0:
        return 0, []
    possible = []
    for key in remaining_keys:
        key_dist, key_inv, key_doors = distances[curr_loc][key]
        locked = len([x for x in key_doors if x.lower() not in inv]) > 0
        if locked:
            continue
        new_inv = inv.copy()
        new_inv.extend([x for x in key_inv if x not in inv])
        new_inv.sort()
        child_dist, path = min_path(key, new_inv, locations, distances)
        new_path = path.copy()
        new_path.insert(0, key)
        possible.append((key_dist + child_dist, new_path.copy()))
    possible.sort(key=lambda x: x[0])
    best_dist, best_path = possible[0]
    seen[(curr_loc, "".join(sorted(inv.copy())))] = (best_dist, best_path)
    return best_dist, best_path


def part_a():
    locations = {}
    start = (-1, -1)
    for row in range(len(pz_input)):
        for col in range(len(pz_input[row])):
            if ord(pz_input[row][col]) in range(ord("a"), ord("z")+1):
                locations[pz_input[row][col]] = (row, col)
            elif pz_input[row][col] == "@":
                start = (row, col)
    distances = defaultdict(lambda: defaultdict(lambda: [0, [], []]))
    keys = [x for x in locations.keys()]
    for i in range(len(locations.keys())):
        dist, found_keys, doors = dist_between(start, locations[keys[i]], pz_input)
        distances["start"][keys[i]] = [dist, found_keys.copy(), doors]
        distances["start"][keys[i]][1].append(keys[i])
        for j in range(i+1, len(locations.keys())):
            dist, found_keys, doors = dist_between(locations[keys[i]], locations[keys[j]], pz_input)
            distances[keys[i]][keys[j]] = [dist, found_keys.copy(), doors]
            distances[keys[i]][keys[j]][1].append(keys[j])
            distances[keys[j]][keys[i]] = [dist, found_keys.copy(), doors]
            distances[keys[j]][keys[i]][1].append(keys[i])
    return min_path("start", [], locations, distances)


def part_b():
    pass


if __name__ == "__main__":
    start = time.process_time()
    print("Part A", part_a())
    mid = time.process_time()
    print(mid - start)
    print("Part B", part_b())
    print(time.process_time() - mid)

