from PuzzleInput import ReadInput
import numpy as np

pz_input = ReadInput(8).data[0]


def part_a():
    values = [int(char) for char in pz_input]
    layers = len(values) // (25 * 6)
    pixels = np.asarray(values)
    pixels.shape = (layers, 6, 25)
    zeros = []
    for i in range(len(pixels)):
        zeros.append(len(pixels[i]) - np.count_nonzero(pixels[i]))
    min_zero_layer = zeros.index(min(zeros))
    return np.count_nonzero(pixels[min_zero_layer] == 1) * np.count_nonzero(pixels[min_zero_layer] == 2)


def part_b():
    values = [int(char) for char in pz_input]
    layers = len(values) // (25 * 6)
    pixels = np.asarray(values)
    pixels.shape = (layers, 6, 25)
    output = pixels[0]
    for i in range(1, len(pixels)):
        for r in range(len(output)):
            for c in range(len(output[r])):
                if output[r, c] == 2:
                    output[r, c] = pixels[i, r, c]
                    if np.count_nonzero(output == 2) == 0:
                        return output
    return output


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B")
    print(part_b())
