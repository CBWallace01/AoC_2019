from PuzzleInput import ReadInput
import networkx as nx

pz_input = ReadInput(20).data


def is_letter(char):
    return ord(char) in range(ord("A"), ord("Z"))


def part_a():
    graph = nx.Graph()
    portals = {}
    for row in range(len(pz_input)):
        if pz_input[row] == "":
            continue
        for col in range(len(pz_input[row])):
            if pz_input[row][col] == "." and (row, col) not in graph:
                graph.add_node((row, col))
            elif is_letter(pz_input[row][col]):
                # Check down
                if is_letter(pz_input[row+1][col]) and pz_input[row+2][col] == ".":
                    if (row+2, col) not in graph:
                        graph.add_node((row+2, col))
                    portal = pz_input[row][col] + pz_input[row+1][col]
                    if portal in portals:
                        graph.add_edge((row, col), portals[portal])
                        del portals[portal]
                    else:
                        portals[portal] = (row, col)


def part_b():
    pass


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())

