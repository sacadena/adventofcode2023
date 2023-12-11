import sys

DIRECTIONS = {
    "S": ('s', 'e', 'n', 'w'),
    ".": (),
    "F": ('s', 'e'),
    "-": ('w', 'e'),
    '7': ('w', 's'),
    '|': ('n', 's'),
    'J': ('n', 'w'),
    'L': ('n', 'e')
}

OPPOSITE = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w'
}


def main():
    with open('data/day10.txt') as h:
        contents = h.readlines()
    matrix = [list(s) for s in contents]
    start_pnt = find_start_point(matrix)
    #loop_length = find_loop_length_recursion(matrix, start_pnt)  # recursion
    loop_length, path = find_loop_length(matrix, start_pnt)  # Stack
    asw1 = loop_length // 2
    print(f'(Puzzle 1) Farthest num steps: {asw1}')
    matrix_path = [
        ['1' if (i, j) in path else '0' for j in range(len(matrix[0]))]
        for i in range(len(matrix))
    ]
    areas_sides = calculate_enclosed_areas(matrix, matrix_path, path[:loop_length], start_pnt)
    print(f'(Puzzle 2) Enclosed area: {min(areas_sides.values())}')


def find_direction(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if y2 > y1 and x2 == x1:
        return 'e'
    if y2 < y1 and x2 == x2:
        return 'w'
    if y2 == y1 and x2 > x1:
        return 's'
    if y2 == y1 and x2 < x1:
        return 'n'
    raise ValueError


def calculate_enclosed_areas(matrix_values, matrix, path, start_pnt):
    def is_valid(node):
        rows, cols = len(matrix), len(matrix[0])
        i, j = node
        if i < 0 or i >= rows or j < 0 or j >= cols:
            return False
        return True

    def get_neighbors_and_dirs(point):
        i, j = point
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        direction_names = ['e', 'w', 's', 'n']
        neighs, dirs = [], []
        for (dx, dy), dir_name in zip(directions, direction_names):
            neigh = (i + dx, j + dy)
            if is_valid(neigh):
                neighs.append(neigh)
                dirs.append(dir_name)
        return neighs, dirs

    def get_sides_map(orientation):
        orders = {'w': "ABAB", "e": "BABA", "n": "ABAB", "s": "BABA"}
        return {_x: _y for _x, _y in zip("nswe", orders[orientation])}

    def update_sides_map(prev_dir, current_value, previous_map):
        new_map = {}
        if current_value == 'F':
            if prev_dir == "w":
                new_map['s'] = new_map['e'] = previous_map['s']
                new_map['n'] = new_map['w'] = previous_map['n']
            if prev_dir == 'n':
                new_map['s'] = new_map['e'] = previous_map['e']
                new_map['n'] = new_map['w'] = previous_map['w']
        if current_value in ('-', '|'):
            new_map = previous_map
        if current_value == '7':
            if prev_dir == "e":
                new_map['s'] = new_map['w'] = previous_map['s']
                new_map['n'] = new_map['e'] = previous_map['n']
            if prev_dir == "n":
                new_map['s'] = new_map['w'] = previous_map['w']
                new_map['n'] = new_map['e'] = previous_map['e']
        if current_value == 'L':
            if prev_dir == "w":
                new_map['s'] = new_map['w'] = previous_map['s']
                new_map['n'] = new_map['e'] = previous_map['n']
            if prev_dir == "s":
                new_map['s'] = new_map['w'] = previous_map['w']
                new_map['n'] = new_map['e'] = previous_map['e']
        if current_value == 'J':
            if prev_dir == "s":
                new_map['s'] = new_map['e'] = previous_map['e']
                new_map['n'] = new_map['w'] = previous_map['w']
            if prev_dir == "e":
                new_map['s'] = new_map['e'] = previous_map['s']
                new_map['n'] = new_map['w'] = previous_map['n']
        return new_map

    sys.setrecursionlimit(1000000)
    visited = set(path)
    prev_point = start_pnt
    areas_total = {'A': 0, 'B': 0}
    dir_init = find_direction(prev_point, path[1])
    current_sides_map = get_sides_map(dir_init)
    for (x, y) in path[1:]:
        neighs, dir_names = get_neighbors_and_dirs((x, y))
        direction = find_direction(prev_point, (x, y))
        prev_point = (x, y)
        current_sides_map = update_sides_map(direction, matrix_values[x][y], current_sides_map)
        for (ni, nj), ori in zip(neighs, dir_names):
            if matrix[ni][nj] == '0' and (ni, nj) not in visited:
                area, visited = calculate_area(matrix, (ni, nj), visited)
                areas_total[current_sides_map[ori]] += area
    return areas_total


def calculate_area(matrix, start_point, visited):
    def flood_fill(point, seen):
        rows, cols = len(matrix), len(matrix[0])
        x, y = point
        if x < 0 or x >= rows or y < 0 or y >= cols or matrix[x][y] != '0' or (x, y) in seen:
            return 0, seen
        seen.add((x, y))
        area = 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            area_here, seen = flood_fill((x + dx, y + dy), seen)
            area += area_here
        return area, seen
    return flood_fill(start_point, visited)


def find_loop_length(matrix, start_pnt):
    num_steps = 0
    stack = [(start_pnt, set(start_pnt), num_steps)]
    path = []
    while stack:
        point, visited, num_steps = stack.pop()
        path.append(point)
        neighbors = get_neighbors(point, matrix)
        if any(matrix[i][j] == 'S' for (i, j) in neighbors) and num_steps > 3:
            return num_steps + 1, path
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            stack.append((neighbor, visited.copy(), num_steps + 1))
    return num_steps, path


def find_loop_length_recursion(matrix, start_pnt):
    def dfs(point, visited, num_steps):
        neighbors = get_neighbors(point, matrix)
        if any(matrix[i][j] == 'S' for (i, j) in neighbors) and num_steps > 2:
            return num_steps + 1
        max_steps = 0
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            steps = dfs(neighbor, visited.copy(), num_steps + 1)
            max_steps = max(max_steps, steps)
        return max_steps
    sys.setrecursionlimit(1000000)
    return dfs(start_pnt, set(), 0)


def get_neighbors(point, matrix):
    num_rows, num_cols = len(matrix), len(matrix[0])
    i, j = point
    current_value = matrix[i][j]
    neighbors = []
    for d, (ni, nj) in zip(
            ('n', 'e', 's', 'w'),
            [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
    ):
        if ni < 0 or ni >= num_rows or nj < 0 or nj >= num_cols:
            continue
        if d in DIRECTIONS[current_value] and OPPOSITE[d] in DIRECTIONS[matrix[ni][nj]]:
            neighbors.append((ni, nj))
    return neighbors


def find_start_point(matrix):
    n, m = len(matrix), len(matrix[0])
    for row in range(n):
        for col in range(m):
            if matrix[row][col] == 'S':
                return row, col
    return None


if __name__ == "__main__":
    main()
