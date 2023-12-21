from collections import deque


def main():
    with open('data/day21.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    matrix = [list(line) for line in contents]
    start_point = find_start_point(matrix)
    asw1 = count_destinations_in_n_steps(matrix, start_point, get_neighbors, 64)
    print(f'(Puzzle 1) Number of final locations after {64}: {asw1}')
    distances_from_start = find_distance_to_start(matrix, start_point)
    asw2 = count_destinations_in_n_steps_efficient(matrix, distances_from_start, 26501365)
    print(f'(Puzzle 2) Number of final locations after {26501365}: {asw2}')


def count_destinations_in_n_steps_efficient(matrix, distances_from_start, n):
    counts_seen = {}

    def count_at_border_tiles(distance, num_steps, num_rows, border_type):
        amt = (num_steps - distance) // num_rows

        if (distance, num_steps, border_type) in counts_seen:
            return counts_seen[(distance, num_steps, border_type)]

        ret = 0
        for x in range(1, amt + 1):
            if (
                    distance + num_rows * x <= num_steps and
                    (distance + num_rows * x) % 2 == (num_steps % 2)
            ):
                if border_type == 'edge':
                    ret += 1
                elif border_type == 'corner':
                    ret += (x + 1)
        counts_seen[(distance, num_steps, border_type)] = ret
        return ret

    count = 0
    num_rows, num_cols = len(matrix), len(matrix[0])
    assert num_rows == num_cols
    options = [-3, -2, -1, 0, 1, 2, 3]

    for row in range(num_rows):
        for col in range(num_cols):
            if (0, 0, row, col) not in distances_from_start:
                continue

            for tx in options:
                for ty in options:
                    d = distances_from_start[(tx, ty, row, col)]
                    if d % 2 == n % 2 and d <= n:
                        count += 1  # interior tiles
                    if tx in [min(options), max(options)] and ty in [min(options), max(options)]:
                        count += count_at_border_tiles(d, n, num_rows, 'corner')
                    elif tx in [min(options), max(options)] or ty in [min(options), max(options)]:
                        count += count_at_border_tiles(d, n, num_rows, 'edge')
    return count


def find_distance_to_start(matrix, start_point):
    num_rows, num_cols = len(matrix), len(matrix[0])
    tile_row, tile_col = 0, 0
    row, col = start_point
    steps = 0
    queue = deque([(tile_row, tile_col, row, col, steps)])
    distances = {}

    while queue:
        tx, ty, x, y, distance = queue.popleft()

        if abs(tx) > 4 or abs(ty) > 4:
            continue  # only compute distance map for tiles within 4 tile steps

        for (nx, ny) in get_neighbors_circular_boundaries(
                (x + tx * num_rows, y + ty * num_cols), matrix
        ):
            tx, ty = nx // num_rows, ny // num_cols
            nx, ny = nx % num_rows, ny % num_cols
            if (tx, ty, nx, ny) in distances:
                continue
            distances[(tx, ty, nx, ny)] = distance + 1
            queue.append((tx, ty, nx, ny, distance + 1))
    return distances


def get_neighbors(point, matrix):
    row, col = point
    neighbors = []
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for dx, dy in directions:
        if 0 <= row + dx < len(matrix) and 0 <= col + dy < len(matrix[0]):
            if matrix[row + dx][col + dy] in ('.', 'S'):
                neighbors.append((row + dx, col + dy))
    return neighbors


def get_neighbors_circular_boundaries(point, matrix):
    row, col = point
    neighbors = []
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for dx, dy in directions:
        x = (row + dx) % len(matrix)
        y = (col + dy) % len(matrix[0])
        if matrix[x][y] in ('.', 'S'):
            neighbors.append((row + dx, col + dy))
    return neighbors


def count_destinations_in_n_steps(
        matrix, start_point, neighbors_getter, n
):
    queue = deque([(start_point, 0)])
    visited = set()
    final_set = set()
    total = 0
    while queue:
        current_point, steps = queue.popleft()

        if steps == n:
            if current_point not in final_set:
                final_set.add(current_point)
                total += 1
            continue

        for neighbor in neighbors_getter(current_point, matrix):
            if (neighbor, steps + 1) in visited:
                continue
            visited.add((neighbor, steps + 1))
            queue.append((neighbor, steps + 1))

    return total


def find_start_point(matrix):
    for i, line in enumerate(matrix):
        for j, char in enumerate(line):
            if char == 'S':
                return i, j


if __name__ == '__main__':
    main()
