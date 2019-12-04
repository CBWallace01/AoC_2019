# No remote puzzle input

pz_min = 158126
pz_max = 624574


def num_to_array(num):
    arr = [0, 0, 0, 0, 0, 0]
    i = 5
    while i >= 0:
        arr[i] = num % 10
        num = num // 10
        i -= 1
    return arr


def valid_number_a(num):
    if (num[0] <= num[1] <= num[2] <= num[3] <= num[4] <= num[5] and
            (num[0] == num[1] or num[1] == num[2] or num[2] == num[3] or num[3] == num[4] or num[4] == num[5])):
        return True
    else:
        return False


def valid_number_b(num):
    if (num[0] <= num[1] <= num[2] <= num[3] <= num[4] <= num[5] and
            ((num[0] == num[1] and num[1] != num[2]) or
             (num[1] == num[2] and num[2] != num[3] and num[1] != num[0]) or
             (num[2] == num[3] and num[3] != num[4] and num[2] != num[1]) or
             (num[3] == num[4] and num[4] != num[5] and num[3] != num[2]) or
             (num[4] == num[5] and num[4] != num[3]))):
        return True
    else:
        return False


def part_a():
    valid = 0
    for i in range(pz_min, pz_max + 1):
        if valid_number_a(num_to_array(i)):
            valid += 1
    return valid


def part_b():
    valid = 0
    for i in range(pz_min, pz_max + 1):
        if valid_number_b(num_to_array(i)):
            valid += 1
    return valid


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
