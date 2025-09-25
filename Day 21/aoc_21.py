def main():
    data = load_file("input_example.txt")
    for line in data:
        for c in line:
            print(c, end="")
        print(end=" ")

def load_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    main()