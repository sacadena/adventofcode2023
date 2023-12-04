from collections import defaultdict


def main():
    with open('data/day04.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    cards = [parse_card(c) for c in contents]
    scores = [get_score_card(card) for card in cards]
    asw1 = sum(scores)
    print(f'(Puzzle 1) Sum: {asw1}')
    nums_per_card = get_nums_per_card(cards)
    asw2 = sum(nums_per_card.values())
    print(f'(Puzzle 2) Num total cards: {asw2}')


def get_nums_per_card(cards):
    nums_per_card = defaultdict(int)
    n_matches = [get_number_matches_card(c) for c in cards]
    i = 0
    while i < len(cards):
        for rep in range(nums_per_card[i] + 1):
            n = n_matches[i]
            for j in range(i + 1, min(i + n + 1, len(cards))):
                nums_per_card[j] += 1
        i += 1

    # add original
    for k in nums_per_card:
        nums_per_card[k] += 1
    return nums_per_card


def parse_card(card_line):
    line = card_line.split(":")[1]
    return line.split('|')[0].split(), line.split('|')[1].split()


def get_number_matches_card(card):
    winning, draws = card
    matches = [int(draw) for draw in draws if draw in winning]
    return len(matches)


def get_score_card(card):
    num_matches = get_number_matches_card(card)
    if num_matches > 0:
        return 2 ** (num_matches - 1)
    return 0


if __name__ == '__main__':
    main()
