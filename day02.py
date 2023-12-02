R, G, B = 12, 13, 14


def main():
    with open('data/day02.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    asw1 = puzzle1(contents)
    print(f'(Puzzle 1) Sum: {asw1}')
    asw2 = puzzle2(contents)
    print(f'(Puzzle 2) Sum Powers: {asw2}')


def parse_draw(draw_line):
    counts = {}
    for ball_count in draw_line.split(","):
        int_str = ball_count.lstrip(" ").rstrip(" ").split(" ")
        counts[int_str[1]] = int(int_str[0])
    return counts


def parse_game(game_line):
    return [parse_draw(draw) for draw in game_line.split(": ")[1].split(";")]


def get_power_game(counts_game):
    max_color = {}
    for color in ('red', 'green', 'blue'):
        max_color[color] = max(c.get(color, 0) for c in counts_game)
    return max(max_color['red'], 1) * max(max_color['green'], 1) * max(max_color['blue'], 1)


def puzzle1(lines):
    counts_games = [parse_game(line) for line in lines]
    possible_game_ids = []
    for i, counts in enumerate(counts_games):
        if any((d.get('blue', 0) > B or d.get('green', 0) > G or d.get('red', 0) > R) for d in counts):
            continue
        possible_game_ids.append(i + 1)
    return sum(possible_game_ids)


def puzzle2(lines):
    counts_games = [parse_game(line) for line in lines]
    power_games = [get_power_game(game) for game in counts_games]
    return sum(power_games)


if __name__ == '__main__':
    main()


