from PuzzleInput import ReadInput

pz_input = ReadInput(5).data[0].split(",")


def part_a():
    a_input = pz_input.copy()
    i = 0
    last_output = None
    while True:
        command = int(a_input[i])
        if command == 99:
            break
        if command % 10 == 1:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            val_1 = int(a_input[int(a_input[i + 1])]) if mode_1 == 0 else int(a_input[i + 1])
            val_2 = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
            loc = int(a_input[i + 3])
            a_input[loc] = val_1 + val_2
            i += 4
        elif command % 10 == 2:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            val_1 = int(a_input[int(a_input[i + 1])]) if mode_1 == 0 else int(a_input[i + 1])
            val_2 = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
            loc = int(a_input[i + 3])
            a_input[loc] = val_1 * val_2
            i += 4
        elif command % 10 == 3:
            a_input[int(a_input[i + 1])] = 1
            i += 2
        elif command % 10 == 4:
            mode = (command // 100) % 10
            if last_output is not None and last_output != 0:
                raise AssertionError("Bad Last Output. Old: %s, New %s, i %s" % (last_output, a_input[int(a_input[i + 1])], i))
            last_output = a_input[int(a_input[i + 1])] if mode == 0 else int(a_input[i + 1])
            i += 2
        else:
            raise AssertionError("Bad command")

    return last_output


def part_b():
    a_input = pz_input.copy()
    i = 0
    last_output = None
    while True:
        command = int(a_input[i])
        if command == 99:
            break
        if command % 10 == 1:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            val_1 = int(a_input[int(a_input[i + 1])]) if mode_1 == 0 else int(a_input[i + 1])
            val_2 = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
            loc = int(a_input[i + 3])
            a_input[loc] = val_1 + val_2
            i += 4
        elif command % 10 == 2:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            val_1 = int(a_input[int(a_input[i + 1])]) if mode_1 == 0 else int(a_input[i + 1])
            val_2 = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
            loc = int(a_input[i + 3])
            a_input[loc] = val_1 * val_2
            i += 4
        elif command % 10 == 3:
            a_input[int(a_input[i + 1])] = 5
            i += 2
        elif command % 10 == 4:
            mode = (command // 100) % 10
            if last_output is not None and last_output != 0:
                raise AssertionError(
                    "Bad Last Output. Old: %s, New %s, i %s" % (last_output, a_input[int(a_input[i + 1])], i))
            last_output = int(a_input[int(a_input[i + 1])]) if mode == 0 else int(a_input[i + 1])
            i += 2
        elif command % 10 == 5:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            if (mode_1 == 0 and int(a_input[int(a_input[i + 1])]) != 0) or (mode_1 == 1 and int(a_input[i + 1]) != 0):
                i = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
                continue
            i += 3
        elif command % 10 == 6:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            if (mode_1 == 0 and int(a_input[int(a_input[i + 1])]) == 0) or (mode_1 == 1 and int(a_input[i + 1]) == 0):
                i = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
                continue
            i += 3
        elif command % 10 == 7:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            mode_3 = (command // 10000) % 10
            val_1 = int(a_input[int(a_input[i + 1])]) if mode_1 == 0 else int(a_input[i + 1])
            val_2 = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
            loc = int(a_input[i + 3])
            a_input[loc] = 1 if val_1 < val_2 else 0
            i += 4
        elif command % 10 == 8:
            mode_1 = (command // 100) % 10
            mode_2 = (command // 1000) % 10
            mode_3 = (command // 10000) % 10
            val_1 = int(a_input[int(a_input[i + 1])]) if mode_1 == 0 else int(a_input[i + 1])
            val_2 = int(a_input[int(a_input[i + 2])]) if mode_2 == 0 else int(a_input[i + 2])
            loc = int(a_input[i + 3])
            a_input[loc] = 1 if val_1 == val_2 else 0
            i += 4
        else:
            raise AssertionError("Bad command %s" % command)

    return last_output


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
