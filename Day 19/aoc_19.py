def main():
    data = load_file("towels.txt")
    towels, combos = get_towels(data)
    towels.sort(key=len)
    possible_counter = 0
    print(towels, data)
    for combo in combos:
        for towel in reversed(towels):
            print(f'combo: {combo}, towel: {towel}')
            combo = combo.replace(towel, '')
        if len(combo) == 0:
            possible_counter += 1
            print("possible!")
        print("\n")
    print(possible_counter)

def get_towels(data):
    towels = data[0].split(", ")
    combos = data[1:]
    return towels, combos

def load_file(path: str):
    file = open(path, 'r')
    data = []
    for line in file:
        if line == "\n":
            continue
        line = line.removesuffix("\n")
        data.append(line)
    return data

if __name__ == "__main__":
    main()