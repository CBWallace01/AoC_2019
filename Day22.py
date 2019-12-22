from PuzzleInput import ReadInput
import networkx as nx

pz_input = ReadInput(22).data


def deal_new(stack):
    stack.reverse()
    return stack


def cut_n(stack, n):
    first = stack[n:]
    second = stack[:n]
    return first + second


def increment_n(stack, n):
    new_stack = [0] * len(stack)
    for i in range(len(stack)):
        new_stack[(i*n) % len(stack)] = stack[i]
    return new_stack


def part_a():
    stack = [x for x in range(10007)]
    for line in pz_input:
        if line == "":
            continue
        pieces = line.split(" ")
        if pieces[0] == "cut":
            stack = cut_n(stack.copy(), int(pieces[1]))
        else:
            if pieces[2] == "increment":
                stack = increment_n(stack.copy(), int(pieces[3]))
            else:
                stack = deal_new(stack.copy())
    return stack.index(2019)


def part_b():
    start_location = 2020
    length = 119315717514047
    seen = []
    i = 0
    needed = 0
    while True:
        curr_location = start_location
        if curr_location in seen:
            needed = i + (101741582076661 % i)
            break
        else:
            seen.append(curr_location)
        i += 1
        for line in pz_input:
            if line == "":
                continue
            pieces = line.split(" ")
            if pieces[0] == "cut":
                n = int(pieces[1])
                if n >= 0:
                    if curr_location < n:
                        curr_location = length - (n - curr_location)
                    else:
                        curr_location -= n
                else:
                    if length - abs(n) > curr_location:
                        curr_location += abs(n)
                    else:
                        curr_location -= length - abs(n)
            else:
                if pieces[2] == "increment":
                    curr_location = (curr_location * int(pieces[3])) % length
                else:
                    curr_location = (length - 1) - curr_location
        start_location = curr_location
    debug = True


if __name__ == "__main__":
    # print("Part A", part_a())
    print("Part B", part_b())

