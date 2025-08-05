from collections import defaultdict

def split_digit(digit: int) -> tuple[int, int]:
    digit_str = str(digit)
    length = len(digit_str)
    mid = length // 2
    left = int(digit_str[:mid])
    right = int(digit_str[mid:])
    return left, right

def blink(stones_count: dict[int, int]) -> dict[int, int]:
    new_stones_count = defaultdict(int)
    for stone, count in stones_count.items():
        if stone == 0:
            new_stones_count[1] += count
            continue
        stone_str = str(stone)
        if len(stone_str) % 2 == 0:
            left_digit, right_digit = split_digit(stone)
            new_stones_count[left_digit] += count
            new_stones_count[right_digit] += count
        else:
            new_stone = stone * 2024
            new_stones_count[new_stone] += count
    return new_stones_count

def main():
    path = "stones.txt"
    stones_count = defaultdict(int)
    stones_file = open(path, 'r')
    for line in stones_file:
        digits = map(int, line.split())
        for digit in digits:
            stones_count[digit] += 1

    blinks = 75
    for i in range(blinks):
        total_stones = sum(stones_count.values())
        print(f"Iteration: {i} | Total stones count: {total_stones}")
        stones_count = blink(stones_count)

    total_stones = sum(stones_count.values())
    print(f"Final total stones count: {total_stones}")

if __name__ == "__main__":
    main()
