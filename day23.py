import sys
from collections import defaultdict
from collections import deque


def main():
    with open('data/day23.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    start_point = (0, [i for i, val in enumerate(contents[0]) if val == '.'][0])
    target_point = (len(contents) - 1, [i for i, val in enumerate(contents[-1]) if val == '.'][0])
    sys.setrecursionlimit(10**7)
    graph = create_graph(contents, start_point, target_point, False)
    asw1 = get_max_of_paths(graph, start_point, target_point)
    print(f'(Puzzle 1) Max length path: {asw1}')
    graph = create_graph(contents, start_point, target_point, True)
    asw2 = get_max_of_paths(graph, start_point, target_point)
    print(f'(Puzzle 2) Max length path: {asw2}')


def get_neighbors(matrix, point):
    row, col = point
    neighbors = []
    for slide, (dr, dc) in zip(('<', '>', '^', 'v'), [(0, -1), (0, 1), (-1, 0), (1, 0)]):
        new_row, new_col = row + dr, col + dc
        if new_row < 0 or new_row >= len(matrix) or new_col < 0 or new_col >= len(matrix[0]):
            continue
        if matrix[new_row][new_col] in (slide, '.'):
            neighbors.append((new_row, new_col))
    return neighbors


def get_neighbors2(matrix, point):
    row, col = point
    neighbors = []
    for (dr, dc) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_row, new_col = row + dr, col + dc
        if new_row < 0 or new_row >= len(matrix) or new_col < 0 or new_col >= len(matrix[0]):
            continue
        if matrix[new_row][new_col] != '#':
            neighbors.append((new_row, new_col))
    return neighbors


def get_max_of_paths(graph, start_point, target_point):
    max_len = 0
    visited = set()

    def dfs(node, d):
        nonlocal max_len
        if node in visited:
            return
        visited.add(node)
        if node == target_point:
            max_len = max(max_len, d)
        for (yd, y) in graph[node]:
            dfs(y, d + yd)
        visited.discard(node)

    dfs(start_point, 0)
    return max_len


def create_graph(matrix, start_point, target_point, ignore_slides):
    vertices = set()
    num_rows, num_cols = len(matrix), len(matrix[0])
    for r in range(num_rows):
        for c in range(num_cols):
            nbr = 0
            for ch, dr, dc in [['^', -1, 0], ['v', 1, 0], ['<', 0, -1], ['>', 0, 1]]:
                if 0 <= r + dr < num_rows and 0 <= c + dc < num_cols and matrix[r + dr][c + dc] != '#':
                    nbr += 1
            if nbr > 2 and matrix[r][c] != '#':
                vertices.add((r, c))

    vertices.add(start_point)
    vertices.add(target_point)

    graph = {}
    for (rv, cv) in vertices:
        graph[(rv, cv)] = []
        queue = deque([(rv, cv, 0)])
        visited = set()
        while queue:
            r, c, d = queue.popleft()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            if (r, c) in vertices and (r, c) != (rv, cv):
                graph[(rv, cv)].append((d, (r, c)))
                continue
            neighbors = get_neighbors2(matrix, (r, c)) if ignore_slides else get_neighbors(matrix, (r, c))
            for (nr, nc) in neighbors:
                queue.append((nr, nc, d + 1))

    return graph


if __name__ == '__main__':
    main()
