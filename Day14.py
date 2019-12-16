from PuzzleInput import ReadInput
import math
from collections import defaultdict

pz_input = ReadInput(14).data
# pz_input = ["157 ORE => 5 NZVS", "165 ORE => 6 DCFZ", "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL", "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ", "179 ORE => 7 PSHF", "177 ORE => 5 HKGWZ", "7 DCFZ, 7 PSHF => 2 XJWVT", "165 ORE => 2 GPVTF", "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"]
# pz_input = ["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG", "17 NVRVD, 3 JNWZP => 8 VPVL", "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL", "22 VJHF, 37 MNCFX => 5 FWMGM", "139 ORE => 4 NVRVD", "144 ORE => 7 JNWZP", "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC", "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV", "145 ORE => 6 MNCFX", "1 NVRVD => 8 CXFTF", "1 VJHF, 6 MNCFX => 4 RFSQX", "176 ORE => 6 VJHF"]
# pz_input = ["171 ORE => 8 CNZTR", "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL", "114 ORE => 4 BHXH", "14 VRPVC => 6 BMBT", "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL", "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT", "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW", "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW", "5 BMBT => 4 WPTQ", "189 ORE => 9 KTJDG", "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP", "12 VRPVC, 27 CNZTR => 2 XDBXC", "15 KTJDG, 12 BHXH => 5 XCVML", "3 BHXH, 2 VRPVC => 7 MZWV", "121 ORE => 7 VRPVC", "7 XCVML => 6 RJRHP", "5 BHXH, 4 VRPVC => 5 LTCX"]
# pz_input = ["9 ORE => 2 A", "8 ORE => 3 B", "7 ORE => 5 C", "3 A, 4 B => 1 AB", "5 B, 7 C => 1 BC", "4 C, 1 A => 1 CA", "2 AB, 3 BC, 4 CA => 1 FUEL"]

reactions = {}
for reaction in pz_input:
    if reaction == "":
        continue
    sides = reaction.split(" => ")
    ingredients = sides[0].split(", ")
    quantities = []
    for i in ingredients:
        stuff = i.split(" ")
        quantities.append((int(stuff[0]), stuff[1]))
    outputs = sides[1].split(" ")
    reactions[outputs[1]] = [int(outputs[0]), quantities]


def find_ore_cost(num_fuel):
    required = defaultdict(lambda: 0)
    extra = defaultdict(lambda: 0)
    required["FUEL"] = num_fuel  # 1877913
    finished = False
    while not finished:
        finished = True
        for elem in required:
            if elem == "ORE" or required[elem] == 0:
                continue
            elif required[elem] > 0:
                finished = False
                to_make = required[elem] - min(required[elem], extra[elem])
                per_reaction = reactions[elem][0]
                num_of_reactions = math.ceil(to_make / per_reaction)
                extra[elem] -= min(required[elem], extra[elem])
                extra[elem] += (num_of_reactions * per_reaction) - to_make
                required[elem] = 0
                for comp in reactions[elem][1]:
                    required[comp[1]] += comp[0] * num_of_reactions
                break
    return required["ORE"]


def part_a():
    return find_ore_cost(1)


def part_b():
    per_fuel = find_ore_cost(1)
    max_num = (1000000000000 // per_fuel) * 2
    min = 1
    max = max_num
    mid_num = ((max-min)//2)+min
    mid = find_ore_cost(mid_num)
    mid_plus = find_ore_cost(mid_num+1)
    while not(mid < 1000000000000 <= mid_plus):
        if mid >= 1000000000000:
            max = ((max-min)//2)+min
        else:
            min = ((max-min)//2)+min
        mid_num = ((max - min) // 2) + min
        mid = find_ore_cost(mid_num)
        mid_plus = find_ore_cost(mid_num + 1)
    return mid_num


if __name__ == "__main__":
    print("Part A", part_a())
    print("Part B", part_b())
