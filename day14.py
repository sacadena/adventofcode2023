from math import gcd
from collections import defaultdict


def main():
    with open('data/day14.txt') as h:
        contents = h.readlines()
    matrix = [c.split('\n')[0] for c in contents]
    matrix_rolled = roll_matrix_direction(matrix, 'north')
    asw1 = score_matrix(matrix_rolled)
    print(f'(Puzzle 1) Total score: {asw1}')
    scores_after_small_n_cycles = get_scores_after_n_cycles(matrix, 700)  # should be high enough n
    period = find_period(scores_after_small_n_cycles, min_period_threshold=5)
    offset = find_offset(scores_after_small_n_cycles, period)
    n_cycles = 1000000000
    asw2 = scores_after_small_n_cycles[offset + ((n_cycles - offset) % period) - 1]
    print(f'(Puzzle 2) Total score after cycles: {asw2}')


def get_scores_after_n_cycles(matrix, n_cycles):
    scores = []
    for i in range(n_cycles):
        matrix = do_cycle(matrix)
        scores.append(score_matrix(matrix))
    return scores


def find_period(sequence, min_period_threshold=5):
    counts = defaultdict(int)
    for s in sequence:
        counts[s] += 1
    counts = dict(counts)
    frequencies = [
        freq for freq in sorted(counts.values(), reverse=True)
        if freq > min_period_threshold
    ]
    unique_frequencies = set(frequencies)
    max_gcd = 1
    for i in unique_frequencies:
        for j in unique_frequencies:
            if i != j:
                max_gcd = max(max_gcd, gcd(i, j))

    for delta in (-1, 0, 1):
        period = (sum(frequencies) // max_gcd) + delta
        if sequence[len(sequence) - period - 1] == sequence[-1]:
            return period
    return len(sequence)


def find_offset(sequence, period):
    offset = 0
    cnt = 0
    for i, val in enumerate(sequence[:-period]):
        if val == sequence[i + period]:
            cnt += 1
            if cnt == period - 1:
                return offset
            continue
        else:
            cnt = 0
            offset = i
    return len(sequence) - 1


def score_matrix(matrix):
    multiplier = len(matrix)
    total = 0
    for row in matrix:
        total += (sum(val == 'O' for val in row) * multiplier)
        multiplier -= 1
    return total


def do_cycle(matrix):
    for direction in ('north', 'west', 'south', 'east'):
        matrix = roll_matrix_direction(matrix, direction)
    return matrix


def roll_matrix_direction(matrix, direction):
    if direction == 'north':
        return transpose_matrix([roll_row(row) for row in transpose_matrix(matrix)])
    if direction == 'west':
        return [roll_row(row) for row in matrix]
    if direction == 'east':
        return flip_matrix([roll_row(row) for row in flip_matrix(matrix)])
    if direction == 'south':
        return transpose_matrix(
            flip_matrix([roll_row(row) for row in flip_matrix(transpose_matrix(matrix))])
        )


def flip_matrix(matrix):
    return [row[::-1] for row in matrix]


def transpose_matrix(m):
    n_rows, n_cols = len(m), len(m[0])
    return [''.join([m[j][i] for j in range(n_rows)]) for i in range(n_cols)]


def roll_row(row):
    stop = 0
    new_row = list(row)
    i = 0
    while i < len(row):
        if row[i] == 'O':
            val = new_row.pop(i)
            new_row.insert(stop, val)
            stop += 1
        if row[i] == "#":
            stop = i + 1
        i += 1
    return ''.join(new_row)


if __name__ == '__main__':
    main()
