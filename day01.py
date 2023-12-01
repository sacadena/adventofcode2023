def main():
    with open('data/day01.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    asw1 = solve_puzzle1(contents)
    print(f'(Puzzle 1) Sum: {asw1}')
    asw2 = solve_puzzle2(contents)
    print(f'(Puzzle 2) Sum: {asw2}')


def find_first_int_character(line):
    numbers = [str(n) for n in range(0, 10)]
    for ch in line:
        if ch in numbers:
            return ch


def first_number_str_or_int(line, numbers_str):
    numbers = [str(n) for n in range(0, 10)]
    mapping = {num_str: ch for ch, num_str in zip(numbers, numbers_str)}
    for i, ch in enumerate(line):
        if ch in numbers:
            return ch
        for num in numbers_str:
            if line[i:].startswith(num):
                return mapping[num]


def solve_puzzle1(lines):
    return sum(
        int(
            find_first_int_character(line) + find_first_int_character(line[::-1])
        )
        for line in lines
    )


def solve_puzzle2(lines):
    numbers_str = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    ]
    numbers_str_rev = [word[::-1] for word in numbers_str]
    return sum(
        int(
            first_number_str_or_int(line, numbers_str) + first_number_str_or_int(line[::-1], numbers_str_rev)
        )
        for line in lines
    )


if __name__ == '__main__':
    main()
