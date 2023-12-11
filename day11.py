def main():
    with open('data/day11.txt') as h:
        contents = h.readlines()
    matrix = [list(c.split('\n')[0]) for c in contents]
    expanded_matrix = expand_matrix(matrix)
    galaxy_locations = identify_locations_galaxies(expanded_matrix)
    minimum_distances = compute_pair_distances(galaxy_locations)
    asw1 = sum(minimum_distances.values())
    print(f'(Puzzle 1) Sum minimum distances: {asw1}')
    original_locations = identify_locations_galaxies(matrix)
    empty_rows, empty_cols = identify_empty_rows_and_cols(matrix)
    updated_locations = update_locations(
        original_locations, empty_rows, empty_cols, multiplier=1000000,
    )
    minimum_distances = compute_pair_distances(updated_locations)
    asw2 = sum(minimum_distances.values())
    print(f'(Puzzle 2) Sum minimum distances: {asw2}')


def update_locations(locations, rows, cols, multiplier):
    updated_locations = []
    for (i, j) in locations:
        ni, nj = i, j
        for r in rows:
            if r < i:
                ni += (multiplier - 1)
        for c in cols:
            if c < j:
                nj += (multiplier - 1)
        updated_locations.append((ni, nj))
    return updated_locations


def identify_empty_rows_and_cols(matrix):
    def _get_empty_rows(m):
        empty_row_ids = []
        for i, row in enumerate(m):
            if all(c == '.' for c in row):
                empty_row_ids.append(i)
        return empty_row_ids
    return _get_empty_rows(matrix), _get_empty_rows(transpose_matrix(matrix))


def minimum_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)


def compute_pair_distances(locations):
    minimum_distances = {}
    for l1 in locations:
        for l2 in locations:
            if l1 != l2 and (l2, l1) not in minimum_distances:
                minimum_distances[(l1, l2)] = minimum_distance(l1, l2)
    return minimum_distances


def identify_locations_galaxies(matrix):
    positions = []
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == '#':
                positions.append((i, j))
    return positions


def transpose_matrix(matrix):
    n_rows, n_cols = len(matrix), len(matrix[0])
    return [[matrix[i][j] for i in range(n_rows)] for j in range(n_cols)]


def expand_matrix(matrix):
    def expand_rows(m):
        new = []
        for row in m:
            if all(c == '.' for c in row):
                new.append(row)
            new.append(row)
        return new
    current = expand_rows(matrix)
    current = transpose_matrix(current)
    current = expand_rows(current)
    return transpose_matrix(current)


if __name__ == "__main__":
    main()
