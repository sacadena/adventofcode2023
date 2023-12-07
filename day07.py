from collections import defaultdict
from functools import cmp_to_key

ORDER_OF_TYPES = [
        "five_of_kind",
        "four_of_kind",
        "full_house",
        "three_of_kind",
        "two_pair",
        "one_pair",
        "high_card",
    ]


def main():
    with open('data/day07.txt') as h:
        contents = h.readlines()
        contents = [c.split('\n')[0] for c in contents]
        hands_bids = parse_contents(contents)
        ordered_hands = find_ordered_hands(hands_bids, comparator1)
        asw1 = sum([(i + 1) * hands_bids[h] for i, h in enumerate(ordered_hands)])
        print(f'(Puzzle 1) Sum rank-weighted bids: {asw1}')
        ordered_hands_jokers = find_ordered_hands(hands_bids, comparator2)
        asw2 = sum([(i + 1) * hands_bids[h] for i, h in enumerate(ordered_hands_jokers)])
        print(f'(Puzzle 2) Sum rank-weighted bids with Jokers: {asw2}')


def find_ordered_hands(hands_bids, comparator):
    return sorted(
        list(hands_bids.keys()),
        key=cmp_to_key(comparator),
        reverse=True,
    )


def count_cards(hand):
    cnt = defaultdict(int)
    for h in hand:
        cnt[h] += 1
    return dict(cnt)


def comparator1(hand1, hand2):
    cmp = not(hand1_higher_than_hand2(
        hand1,
        hand2,
        find_hand_type,
        hand1_higher_than_hand2_based_on_high_card
    ))
    if cmp:
        return 1
    else:
        return -1


def comparator2(hand1, hand2):
    cmp = not (hand1_higher_than_hand2(
        hand1,
        hand2,
        find_hand_type_jokers,
        h1_higher_than_h2_based_on_high_card_jokers
    ))
    if cmp:
        return 1
    else:
        return -1


def hand1_higher_than_hand2(
        hand1, hand2, find_hand_type_func, comparator_higher_card
):
    ind1 = ORDER_OF_TYPES.index(find_hand_type_func(hand1))
    ind2 = ORDER_OF_TYPES.index(find_hand_type_func(hand2))
    if ind1 < ind2:
        return True
    if ind1 > ind2:
        return False
    return comparator_higher_card(hand1, hand2)


def hand1_higher_than_hand2_based_on_high_card(hand1, hand2):
    order_cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    for c1, c2 in zip(hand1, hand2):
        if order_cards.index(c1) < order_cards.index(c2):
            return True
        if order_cards.index(c1) > order_cards.index(c2):
            return False
    return False


def find_hand_type(hand):
    cnt = count_cards(hand)
    if len(cnt) == 1:
        return "five_of_kind"
    if any(v == 4 for v in cnt.values()):
        return "four_of_kind"
    if len(cnt) == 2:
        return "full_house"
    if any(v == 3 for v in cnt.values()):
        return "three_of_kind"
    if len(cnt) == 3:
        return "two_pair"
    if any(v == 2 for v in cnt.values()):
        return "one_pair"
    return "high_card"


def find_hand_type_jokers(hand: str):
    if hand == "JJJJJ":
        return "five_of_kind"
    if "J" in hand:
        hand_options = [hand.replace('J', card) for card in hand if card != 'J']
        return min([find_hand_type(h) for h in hand_options], key=ORDER_OF_TYPES.index)
    return find_hand_type(hand)


def h1_higher_than_h2_based_on_high_card_jokers(hand1, hand2):
    order_cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    for c1, c2 in zip(hand1, hand2):
        if order_cards.index(c1) < order_cards.index(c2):
            return True
        if order_cards.index(c1) > order_cards.index(c2):
            return False
    return False


def parse_contents(contents):
    hands_bids = {}
    for line in contents:
        hand, bid = line.split()
        hands_bids[hand] = int(bid)
    return hands_bids


if __name__ == "__main__":
    main()
