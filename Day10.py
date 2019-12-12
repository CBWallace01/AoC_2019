from PuzzleInput import ReadInput

pz_input = ReadInput(10).data


def part_a():
    asteroids = []
    for i in range(len(pz_input)):
        for j in range(len(pz_input[i])):
            if pz_input[i][j] == "#":
                asteroids.append((j, i))
    count = 0
    location = (-1, -1)
    for asteroid in asteroids:
        visible = 0
        for to_test in asteroids:
            if asteroid == to_test:
                continue
            test_slope = (to_test[1] - asteroid[1]) / (to_test[0] - asteroid[0]) if to_test[0] - asteroid[0] != 0 else None
            valid = True
            for check_interfere in asteroids:
                is_between = min(asteroid[0], to_test[0]) <= check_interfere[0] <= max(asteroid[0], to_test[0]) and min(asteroid[1], to_test[1]) <= check_interfere[1] <= max(asteroid[1], to_test[1])
                if not is_between or check_interfere == to_test or check_interfere == asteroid:
                    continue
                interference_slope = (check_interfere[1] - asteroid[1]) / (check_interfere[0] - asteroid[0]) if check_interfere[0] - asteroid[0] != 0 else None
                if test_slope == interference_slope:
                    valid = False
                    break
            if valid:
                visible += 1
        if visible > count:
            count = visible
            location = asteroid
    return location, count


def part_b():
    station = (11, 13)
    asteroids = []
    for i in range(len(pz_input)):
        for j in range(len(pz_input[i])):
            if pz_input[i][j] == "#" and not (j == 11 and i == 13):
                asteroids.append((j, i))
    destroyed = 0
    while True:
        visible = []
        for to_test in asteroids:
            if station == to_test:
                continue
            test_slope = (to_test[1] - station[1]) / (to_test[0] - station[0]) if to_test[0] - station[0] != 0 else None
            valid = True
            for check_interfere in asteroids:
                is_between = min(station[0], to_test[0]) <= check_interfere[0] <= max(station[0], to_test[0]) and min(
                    station[1], to_test[1]) <= check_interfere[1] <= max(station[1], to_test[1])
                if not is_between or check_interfere == to_test or check_interfere == station:
                    continue
                interference_slope = (check_interfere[1] - station[1]) / (check_interfere[0] - station[0]) if \
                check_interfere[0] - station[0] != 0 else None
                if test_slope == interference_slope:
                    valid = False
                    break
            if valid:
                visible.append((to_test, test_slope))
        up = [x for x in visible if x[0][0] == station[0] and x[0][1] < station[1]][0]
        asteroids.remove(up[0])
        destroyed += 1
        if destroyed == 200:
            return up[0][0] * 100 + up[0][1]
        quad_1 = [x for x in visible if x[0][0] > station[0] and x[0][1] < station[1]]
        quad_1.sort(key=lambda x: x[1])
        for q_1_destroyed in quad_1:
            asteroids.remove(q_1_destroyed[0])
            destroyed += 1
            if destroyed == 200:
                return q_1_destroyed[0][0] * 100 + q_1_destroyed[0][1]
        right = [x for x in visible if x[0][0] > station[0] and x[0][1] == station[1]][0]
        asteroids.remove(right[0])
        destroyed += 1
        if destroyed == 200:
            return right[0][0] * 100 + right[0][1]
        quad_2 = [x for x in visible if x[0][0] > station[0] and x[0][1] > station[1]]
        quad_2.sort(key=lambda x: x[1])
        for q_2_destroyed in quad_2:
            asteroids.remove(q_2_destroyed[0])
            destroyed += 1
            if destroyed == 200:
                return q_2_destroyed[0][0] * 100 + q_2_destroyed[0][1]
        down = [x for x in visible if x[0][0] == station[0] and x[0][1] > station[1]][0]
        asteroids.remove(down[0])
        destroyed += 1
        if destroyed == 200:
            return down[0][0] * 100 + down[0][1]
        quad_3 = [x for x in visible if x[0][0] < station[0] and x[0][1] > station[1]]
        quad_3.sort(key=lambda x: x[1], reverse=True)
        for q_3_destroyed in quad_3:
            asteroids.remove(q_3_destroyed[0])
            destroyed += 1
            if destroyed == 200:
                return q_3_destroyed[0][0] * 100 + q_3_destroyed[0][1]
        left = [x for x in visible if x[0][0] < station[0] and x[0][1] == station[1]][0]
        asteroids.remove(left[0])
        destroyed += 1
        if destroyed == 200:
            return left[0][0] * 100 + left[0][1]
        quad_4 = [x for x in visible if x[0][0] < station[0] and x[0][1] < station[1]]
        quad_4.sort(key=lambda x: x[1])
        for q_4_destroyed in quad_4:
            asteroids.remove(q_4_destroyed[0])
            destroyed += 1
            if destroyed == 200:
                return q_4_destroyed[0][0] * 100 + q_4_destroyed[0][1]


if __name__ == "__main__":
    # print("Part A", part_a())
    print("Part B", part_b())
