from PuzzleInput import ReadInput

pz_input = ReadInput(16).data[0]
input_arr = [int(x) for x in pz_input]
# input_arr = [int(x) for x in "80871224585914546619083218645595"]


def part_a():
    base_pattern = [0, 1, 0, -1]
    phase_input = input_arr.copy()
    # num of phases
    for i in range(100):
        next_input = phase_input.copy()
        # calculating new value for each index
        for j in range(len(phase_input)):
            j_pattern = []
            value = 0
            for elem in base_pattern:
                for x in range(j+1):
                    j_pattern.append(elem)
            # iterate through each item
            for k in range(len(phase_input)):
                value += phase_input[k] * j_pattern[(k+1)%len(j_pattern)]
            next_input[j] = abs(value) % 10
        phase_input = next_input
    return phase_input[:8]


def part_b():
    phase_input = input_arr.copy()
    # num of phases
    for i in range(100):
        next_input = phase_input.copy()
        # calculating new value for each index
        for j in range(len(phase_input)):
            value = 0
            positives = [x for x in range(len(phase_input) * 10000) if x % (4 * (j+1)) == i]
            next_input[j] = abs(value) % 10
        phase_input = next_input
    return phase_input[:8]


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())

# Notes:
# 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0

# 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0 [0,1,0,-1] 1 = index%4 == 0; -1 = index%4 == 2
# 0 1 1 0 0-1-1 0 0 1 1 0 0-1-1 0 0 1 1 0 0-1-1 0 0 1 1 0 0-1 [0,0,1,1,0,0,-1,-1] 1 = index%8 == 1,2; -1 = index%8 == 5,6
# 0 0 1 1 1 0 0 0-1-1-1 0 0 0 1 1 1 0 0 0-1-1-1 0 0 0 1 1 1 0 [0,0,0,1,1,1,0,0,0,-1,-1,-1] 1 = index%12 == 2,3,4; -1 = index%8 == 8,9,10
# 0 0 0 1 1 1 1 0 0 0 0-1-1-1-1 0 0 0 0 1 1 1 1 0 0 0 0-1-1-1 -1 => 11, 12, 13, 14 ... 27
# 0 0 0 0 1 1 1 1 1 0 0 0 0 0-1-1-1-1-1 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0-1-1-1-1-1

# 0>3, 1>6, 2>9
# 0>2, 1>5, 2>8, 3>11, 4>14
# index % (3 * (i+1)) ==

# 1 => index % (4 *(i+1)) == i
# find start using ^
# range = start + i + 1
