from PuzzleInput import ReadInput
import time
import numpy as np
from collections import defaultdict
import heapq

# pz_input = np.array([list(x) for x in ReadInput(18).data if x != ''])
# pz_input = np.array([list(x) for x in ["#########", "#b.A.@.a#", "#########"]])
# pz_input = np.array([list(x) for x in ["########################", "#f.D.E.e.C.b.A.@.a.B.c.#", "######################.#", "#d.....................#", "########################"]])
# pz_input = np.array([list(x) for x in ["########################", "#...............b.C.D.f#", "#.######################", "#.....@.a.B.c.d.A.e.F.g#", "########################"]])
pz_input = np.array([list(x) for x in ["#################", "#i.G..c...e..H.p#", "########.########", "#j.A..b...f..D.o#", "########@########", "#k.E..a...g..B.n#", "########.########", "#l.F..d...h..C.m#", "#################"]])
# pz_input = np.array([list(x) for x in ["########################", "#@..............ac.GI.b#", "###d#e#f################", "###A#B#C################", "###g#h#i################", "########################"]])


def part_a():
    # Key: symbol, Value: Location
    locations = {}
    for row in range(pz_input.shape[0]):
        for col in range(pz_input.shape[1]):
            if pz_input[row, col] not in '#.':
                locations[pz_input[row, col]] = (row, col)
    # Key: "{symbol}-{symbol}", Value: [Distance, [Requirements]]
    connections = {}
    min_connections = defaultdict(lambda: np.inf)
    # Build Path and record Requirements
    symbols = list(locations.keys())
    for i in range(len(locations)):
        for j in range(i+1, len(locations)):
            start_symbol = symbols[i]
            end_symbol = symbols[j]
            if start_symbol == end_symbol:
                continue
            end_row, end_col = locations[end_symbol]
            visited = []
            paths = [(abs(end_row - locations[start_symbol][0]) + abs(end_col - locations[start_symbol][1]), [locations[start_symbol]], [])]
            heapq.heapify(paths)
            correct_path = None
            requirements = None
            while True:
                _, curr_path, curr_req = heapq.heappop(paths)
                for neighbor in range(-1, 2, 2):
                    if pz_input[curr_path[-1][0] + neighbor, curr_path[-1][1]] in visited or (curr_path[-1][0] + neighbor, curr_path[-1][1]) in curr_path:
                        pass
                    elif pz_input[curr_path[-1][0] + neighbor, curr_path[-1][1]] == end_symbol:
                        correct_path = curr_path.copy()
                        correct_path.append((curr_path[-1][0] + neighbor, curr_path[-1][1]))
                        requirements = curr_req
                        break
                    elif pz_input[curr_path[-1][0] + neighbor, curr_path[-1][1]] != '#':
                        new_req = None
                        if ord(pz_input[curr_path[-1][0] + neighbor, curr_path[-1][1]]) in range(ord('A'), ord('Z')+1):
                            new_req = chr((ord(pz_input[curr_path[-1][0] + neighbor, curr_path[-1][1]]) - ord('A')) + ord('a'))
                        new_path = curr_path.copy()
                        new_path.append((curr_path[-1][0] + neighbor, curr_path[-1][1]))
                        new_req_list = curr_req.copy()
                        if new_req is not None:
                            new_req_list.append(new_req)
                        heapq.heappush(paths, (len(new_path) + abs(end_row - new_path[-1][0]) + abs(end_col - new_path[-1][1]), new_path, new_req_list))

                    if pz_input[curr_path[-1][0], curr_path[-1][1] + neighbor] in visited or (curr_path[-1][0], curr_path[-1][1] + neighbor) in curr_path:
                        pass
                    elif pz_input[curr_path[-1][0], curr_path[-1][1] + neighbor] == end_symbol:
                        correct_path = curr_path.copy()
                        correct_path.append((curr_path[-1][0], curr_path[-1][1] + neighbor))
                        requirements = curr_req
                        break
                    elif pz_input[curr_path[-1][0], curr_path[-1][1] + neighbor] != '#':
                        new_req = None
                        if ord(pz_input[curr_path[-1][0], curr_path[-1][1] + neighbor]) in range(ord('A'), ord('Z')+1):
                            new_req = chr((ord(pz_input[curr_path[-1][0], curr_path[-1][1] + neighbor]) - ord('A')) + ord('a'))
                        new_path = curr_path.copy()
                        new_path.append((curr_path[-1][0], curr_path[-1][1] + neighbor))
                        new_req_list = curr_req.copy()
                        if new_req is not None:
                            new_req_list.append(new_req)
                        heapq.heappush(paths, (len(new_path) + abs(end_row - new_path[-1][0]) + abs(end_col - new_path[-1][1]), new_path, new_req_list))
                    visited.append(curr_path[-1])
                if correct_path is not None:
                    break
            connections[f"{start_symbol}-{end_symbol}"] = (len(correct_path)-1, requirements)
            connections[f"{end_symbol}-{start_symbol}"] = (len(correct_path) - 1, requirements)
            min_connections[start_symbol] = min(min_connections[start_symbol], len(correct_path)-1)
            min_connections[end_symbol] = min(min_connections[end_symbol], len(correct_path) - 1)
    # Build routes
    in_progress_routes = [(0, 0, ['@'])]
    heapq.heapify(in_progress_routes)
    complete_routes = []
    visited = []
    while len(in_progress_routes) > 0:
        _, curr_dist, curr_path = heapq.heappop(in_progress_routes)
        if len(complete_routes) > 0 and curr_dist >= min(complete_routes):
            continue
        for symbol in [x for x in locations if x not in curr_path]:
            # Don't go to a locked door
            if ord(symbol) in range(ord('A'), ord('Z')+1) and chr((ord(symbol) - ord('A')) + ord('a')) not in curr_path:
                continue
            met_requirements = True
            # Be sure all intermediate requirements are met
            for requirement in connections[f"{curr_path[-1]}-{symbol}"][1]:
                if requirement not in curr_path:
                    met_requirements = False
                    break
            if not met_requirements:
                continue
            new_route = curr_path.copy()
            new_route.append(symbol)
            new_dist = curr_dist + connections[f"{curr_path[-1]}-{symbol}"][0]
            if len(new_route) == len(locations) and not (len(complete_routes) > 0 and new_dist >= min(complete_routes)):
                complete_routes.append(new_dist)
            elif (new_route, new_dist) not in in_progress_routes and not (len(complete_routes) > 0 and new_dist >= min(complete_routes)):
                heapq.heappush(in_progress_routes, (new_dist + ((len(locations) - len(new_route)) ** 2), new_dist, new_route))
    return min(complete_routes)


def part_b():
    pass


if __name__ == "__main__":
    start = time.process_time()
    print("Part A", part_a())
    mid = time.process_time()
    print(mid - start)
    print("Part B", part_b())
    print(time.process_time() - mid)

