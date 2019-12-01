from PuzzleInput import ReadInput

pz_input = ReadInput(1).data

# Part 1
total = 0

for mass in pz_input:
    if mass == "":
        continue
    total += (int(mass) // 3) - 2

print(total)


# Part 2
def calculate_fuel(weight):
    fuel = (weight // 3) - 2
    return max(fuel, 0)


total = 0

for mass in pz_input:
    if mass == "":
        continue
    mass_val = int(mass)
    fuel = calculate_fuel(mass_val)
    while fuel > 0:
        total += fuel
        fuel = calculate_fuel(fuel)

print(total)
