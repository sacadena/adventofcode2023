import sys


def main():
    with open('data/day16.txt') as h:
        contents = h.readlines()

    sys.setrecursionlimit(10000)
    matrix = [list(line.strip()) for line in contents]
    cells_directions = get_cells_directions(matrix, (0, 0, 'right'))
    asw1 = num_unique_positions(cells_directions)
    print(f'(Puzzle 1) Unique visited cells: {asw1}')
    candidate_position_directions = find_initial_points_and_directions(len(matrix), len(matrix[0]))
    asw2 = max(num_unique_positions(get_cells_directions(matrix, c)) for c in candidate_position_directions)
    print(f'(Puzzle 2) Max number of unique visited cells: {asw2}')


def find_initial_points_and_directions(rows, cols):
    candidates = []
    for row in range(rows):
        candidates.append((row, 0, 'right'))
        candidates.append((row, cols - 1, 'left'))
    for col in range(cols):
        candidates.append((0, col, 'down'))
        candidates.append((rows - 1, col, 'up'))
    return candidates


def num_unique_positions(cells_directions):
    unique_visited_cells = set((r, c) for r, c, d in cells_directions)
    return len(unique_visited_cells)


def get_neighbors(val, point, arrow_direction):
    row, col = point
    neighbors = []
    if arrow_direction == 'up':
        if val in ('|', '.'):
            neighbors.append((row - 1, col, 'up'))
        elif val == '-':
            neighbors.append((row, col - 1, 'left'))
            neighbors.append((row, col + 1, 'right'))
        elif val == '/':
            neighbors.append((row, col + 1, 'right'))
        elif val == '\\':
            neighbors.append((row, col - 1, 'left'))
    elif arrow_direction == 'down':
        if val in ('|', '.'):
            neighbors.append((row + 1, col, 'down'))
        elif val == '-':
            neighbors.append((row, col - 1, 'left'))
            neighbors.append((row, col + 1, 'right'))
        elif val == '/':
            neighbors.append((row, col - 1, 'left'))
        elif val == '\\':
            neighbors.append((row, col + 1, 'right'))
    elif arrow_direction == 'right':
        if val == '|':
            neighbors.append((row - 1, col, 'up'))
            neighbors.append((row + 1, col, 'down'))
        elif val in ('-', '.'):
            neighbors.append((row, col + 1, 'right'))
        elif val == '/':
            neighbors.append((row - 1, col, 'up'))
        elif val == '\\':
            neighbors.append((row + 1, col, 'down'))
    elif arrow_direction == 'left':
        if val == '|':
            neighbors.append((row - 1, col, 'up'))
            neighbors.append((row + 1, col, 'down'))
        elif val in ('-', '.'):
            neighbors.append((row, col - 1, 'left'))
        elif val == '/':
            neighbors.append((row + 1, col, 'down'))
        elif val == '\\':
            neighbors.append((row - 1, col, 'up'))

    return neighbors


def get_cells_directions(matrix, start_point):
    def is_valid(point_direction):
        row, col, direction = point_direction
        if row < 0 or col < 0 or row >= len(matrix) or col >= len(matrix[0]):
            return False
        return True

    table = set()

    def dfs(point_direction, visited):
        row, col, direction = point_direction
        if point_direction in table:
            return

        neighbors = [
            neigh for neigh in get_neighbors(matrix[row][col], (row, col), direction)
            if is_valid(neigh)
        ]
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            dfs(neighbor, visited)

        table.add(point_direction)

    seen = {start_point}
    dfs(start_point, seen)
    return seen


if __name__ == '__main__':
    main()
