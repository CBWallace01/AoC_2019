from PuzzleInput import ReadInput
import numpy as np
from collections import defaultdict
import heapq

pz_input = [x for x in ReadInput(20).data if x != '']
print(pz_input)
# pz_input = ['         A           ',
#             '         A           ',
#             '  #######.#########  ',
#             '  #######.........#  ',
#             '  #######.#######.#  ',
#             '  #######.#######.#  ',
#             '  #######.#######.#  ',
#             '  #####  B    ###.#  ',
#             'BC...##  C    ###.#  ',
#             '  ##.##       ###.#  ',
#             '  ##...DE  F  ###.#  ',
#             '  #####    G  ###.#  ',
#             '  #########.#####.#  ',
#             'DE..#######...###.#  ',
#             '  #.#########.###.#  ',
#             'FG..#########.....#  ',
#             '  ###########.#####  ',
#             '             Z       ',
#             '             Z       ']


def part_a():
    portals = defaultdict(lambda: [])
    start_loc = None
    end_loc = None
    for row in range(len(pz_input)):
        for col in range(len(pz_input[0])):
            if pz_input[row][col] in '.# ':
                continue
            portal_key = None
            portal_point = None
            if row + 1 < len(pz_input) and ord(pz_input[row+1][col]) in range(ord('A'), ord('Z')+1):
                portal_key = pz_input[row][col] + pz_input[row+1][col]
                portal_point = (row + 2, col) if row + 2 < len(pz_input) and pz_input[row + 2][col] == '.' else (row - 1, col)
            elif col + 1 < len(pz_input[0]) and ord(pz_input[row][col+1]) in range(ord('A'), ord('Z')+1):
                portal_key = pz_input[row][col] + pz_input[row][col+1]
                portal_point = (row, col + 2) if col + 2 < len(pz_input[0]) and pz_input[row][col + 2] == '.' else (row, col - 1)
            if portal_key == 'AA':
                start_loc = portal_point
            elif portal_key == 'ZZ':
                end_loc = portal_point
            elif portal_key is not None:
                portals[portal_key].append(portal_point)
    in_progress_paths = [(0, [start_loc])]
    heapq.heapify(in_progress_paths)
    visited = []
    while True:
        _, curr_path = heapq.heappop(in_progress_paths)
        for neighbor in [(curr_path[-1][0] - 1, curr_path[-1][1]), (curr_path[-1][0] + 1, curr_path[-1][1]),
                         (curr_path[-1][0], curr_path[-1][1] - 1), (curr_path[-1][0], curr_path[-1][1] + 1)]:
            if pz_input[neighbor[0]][neighbor[1]] == '#':
                continue
            if ord(pz_input[neighbor[0]][neighbor[1]]) in range(ord('A'), ord('Z')+1):
                relevant = [x for x in portals.values() if curr_path[-1] in x]
                if len(relevant) == 0:
                    continue
                portal_locs = [y for y in relevant[0] if y != curr_path[-1]]
                if len(portal_locs) > 0:
                    neighbor = portal_locs[0]
                else:
                    continue
            if neighbor == end_loc:
                return len(curr_path)
            elif neighbor not in curr_path and neighbor not in visited:
                new_path = curr_path.copy()
                new_path.append(neighbor)
                heapq.heappush(in_progress_paths, (len(new_path), new_path))


def part_b():
    pass


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
