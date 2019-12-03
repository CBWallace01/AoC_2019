from PuzzleInput import ReadInput


def check_intersect(seg_1, seg_2):
    seg_1_is_vert = seg_1[0] == seg_1[2]
    seg_2_is_vert = seg_2[0] == seg_2[2]
    intersects = ((seg_1_is_vert != seg_2_is_vert) and
                  ((seg_1_is_vert and min(seg_2[0], seg_2[2]) <= seg_1[0] <= max(seg_2[0], seg_2[2]) and min(seg_1[1], seg_1[3]) <= seg_2[1] <= max(seg_1[1], seg_1[3])) or
                   (seg_2_is_vert and min(seg_1[0], seg_1[2]) <= seg_2[0] <= max(seg_1[0], seg_1[2]) and min(seg_2[1], seg_2[3]) <= seg_1[1] <= max(seg_2[1], seg_2[3]))))
    dist = abs(seg_1[0]) + abs(seg_2[1]) if intersects and seg_1_is_vert else \
        abs(seg_2[0]) + abs(seg_1[1]) if intersects and seg_2_is_vert else None
    point = (seg_1[0], seg_2[1]) if intersects and seg_1_is_vert else \
        (seg_2[0], seg_1[1]) if intersects and seg_2_is_vert else None
    return intersects, dist, point


def part_a():
    pz_input = ReadInput(3).data
    wire_segments = []
    min_dist = None
    for wire in pz_input:
        x = 0
        y = 0
        new_segments = []
        moves = wire.split(",")
        for move in moves:
            if move == "":
                continue
            new_x = x
            new_y = y
            if move[0] == "R":
                new_x += int(move[1:])
            elif move[0] == "L":
                new_x -= int(move[1:])
            elif move[0] == "U":
                new_y += int(move[1:])
            elif move[0] == "D":
                new_y -= int(move[1:])
            new_segments.append((x, y, new_x, new_y))
            x = new_x
            y = new_y
        wire_segments.append(new_segments)
    for i in wire_segments[0]:
        for j in wire_segments[1]:
            does_intersect, dist, point = check_intersect(i, j)
            if does_intersect and (min_dist is None or dist < min_dist) and dist > 0:
                min_dist = dist
    return min_dist


def part_b():
    pz_input = ReadInput(3).data
    wire_segments = []
    min_dist = None
    for wire in pz_input:
        x = 0
        y = 0
        new_segments = []
        moves = wire.split(",")
        for move in moves:
            if move == "":
                continue
            new_x = x
            new_y = y
            if move[0] == "R":
                new_x += int(move[1:])
            elif move[0] == "L":
                new_x -= int(move[1:])
            elif move[0] == "U":
                new_y += int(move[1:])
            elif move[0] == "D":
                new_y -= int(move[1:])
            new_segments.append((x, y, new_x, new_y))
            x = new_x
            y = new_y
        wire_segments.append(new_segments)
    for i in wire_segments[0]:
        for j in wire_segments[1]:
            does_intersect, dist, point = check_intersect(i, j)
            if does_intersect:
                wire_1 = 0
                wire_2 = 0
                for m in wire_segments[0]:
                    if m[0] == m[2] and m[2] == point[0] and min(m[1], m[3]) <= point[1] <= max(m[1], m[3]):
                        wire_1 += abs(point[1] - m[1])
                        break
                    elif m[1] == m[3] and m[3] == point[1] and min(m[0], m[2]) <= point[0] <= max(m[0], m[2]):
                        wire_1 += abs(point[0] - m[0])
                        break
                    else:
                        wire_1 += abs(m[2] - m[0]) + abs(m[3] - m[1])
                for n in wire_segments[1]:
                    if n[0] == n[2] and n[2] == point[0] and min(n[1], n[3]) <= point[1] <= max(n[1], n[3]):
                        wire_2 += abs(point[1] - n[1])
                        break
                    elif n[1] == n[3] and n[3] == point[1] and min(n[0], n[2]) <= point[0] <= max(n[0], n[2]):
                        wire_2 += abs(point[0] - n[0])
                        break
                    else:
                        wire_2 += abs(n[2] - n[0]) + abs(n[3] - n[1])
                if min_dist is None or wire_1 + wire_2 < min_dist:
                    min_dist = wire_1 + wire_2
    return min_dist


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
