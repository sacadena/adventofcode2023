def main():
    with open('data/day13.txt') as h:
        contents = h.read()
    islands = [island.split('\n') for island in contents.split('\n\n')]
    scores = [score_island(island) for island in islands]
    asw1 = sum(scores)
    print(f'(Puzzle 1) Total score: {asw1}')
    scores = [score_island_with_fudge(island) for island in islands]
    asw2 = sum(scores)
    print(f'(Puzzle 1) Total score with smudge: {asw2}')


def transpose_matrix(m):
    n_rows, n_cols = len(m), len(m[0])
    return [''.join([m[j][i] for j in range(n_rows)]) for i in range(n_cols)]


def find_mirror(m):
    for i in range(1, len(m)):
        if m[i - 1] == m[i]:
            left, right = i - 1, i
            while True:
                if left == 0 or right == len(m)-1:
                    if m[left] == m[right]:
                        return (i - 1) + 1  # rows numbered from 1
                    break
                if m[left] == m[right]:
                    right += 1
                    left -= 1
                else:
                    break
    return 0


def is_equal_but_one(row1, row2):
    return sum(r1 != r2 for r1, r2 in zip(row1, row2)) == 1


def find_mirror_with_smudge(m):
    for i in range(1, len(m)):
        num_smudge = 0
        if m[i - 1] == m[i] or is_equal_but_one(m[i - 1], m[i]):
            left, right = i - 1, i
            while True:
                if left == 0 or right == len(m)-1:
                    if m[left] == m[right] or is_equal_but_one(m[left], m[right]):
                        num_smudge = num_smudge + 1 if is_equal_but_one(m[left], m[right]) else num_smudge
                        if num_smudge == 1:
                            return (i - 1) + 1  # rows numbered from 1
                        break
                if (m[left] == m[right]) or is_equal_but_one(m[left], m[right]):
                    num_smudge = num_smudge + 1 if is_equal_but_one(m[left], m[right]) else num_smudge
                    if num_smudge > 1:
                        break
                    right += 1
                    left -= 1
                else:
                    break
    return 0


def score_island(island):
    transposed_island = transpose_matrix(island)
    h = find_mirror(island)
    v = find_mirror(transposed_island)
    return v + (100 * h)


def score_island_with_fudge(island):
    transposed_island = transpose_matrix(island)
    h = find_mirror_with_smudge(island)
    v = find_mirror_with_smudge(transposed_island)
    return v + (100 * h)


if __name__ == "__main__":
    main()
