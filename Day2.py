from PuzzleInput import ReadInput

pz_input = ReadInput(2).data[0].split(",")

# Part 1
# pz_input[1] = 12
# pz_input[2] = 2
# for i in range(0, len(pz_input), 4):
#     command = int(pz_input[i])
#     if command == 99:
#         break
#     loc_1 = int(pz_input[i + 1])
#     loc_2 = int(pz_input[i + 2])
#     loc_3 = int(pz_input[i + 3])
#     pz_input[loc_3] = (int(pz_input[loc_1]) + int(pz_input[loc_2])) if command == 1 else (int(pz_input[loc_1]) * int(pz_input[loc_2]))

# print(pz_input)

# Part 2
for n in range(0, 100):
    for v in range(0, 100):
        cp_input = pz_input.copy()
        cp_input[1] = n
        cp_input[2] = v
        for i in range(0, len(cp_input), 4):
            command = int(cp_input[i])
            if command == 99:
                break
            loc_1 = int(cp_input[i + 1])
            loc_2 = int(cp_input[i + 2])
            loc_3 = int(cp_input[i + 3])
            cp_input[loc_3] = (int(cp_input[loc_1]) + int(cp_input[loc_2])) if command == 1 else (int(cp_input[loc_1]) * int(cp_input[loc_2]))
        if cp_input[0] == 19690720:
            print((100 * int(cp_input[1])) + cp_input[2])
