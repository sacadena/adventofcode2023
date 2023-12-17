from heapq import heappush, heappop


def main():
    with open('data/day17.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    matrix = [list(map(int, line)) for line in contents]
    asw1 = find_lowest_cost_restriction(matrix, 3)
    print(f'(Puzzle 1) Lowest cost: {asw1}')
    asw2 = find_lowest_cost_restriction(matrix, 10, 4)
    print(f'(Puzzle 2) Lowest cost: {asw2}')


def get_neighbors(point_dir):
    row, col, direction = point_dir
    if direction == 'N':
        return [(row - 1, col, 'N'), (row, col - 1, 'W'), (row, col + 1, 'E')]
    elif direction == 'S':
        return [(row + 1, col, 'S'), (row, col - 1, 'W'), (row, col + 1, 'E')]
    elif direction == 'W':
        return [(row, col - 1, 'W'), (row - 1, col, 'N'), (row + 1, col, 'S')]
    elif direction == 'E':
        return [(row, col + 1, 'E'), (row - 1, col, 'N'), (row + 1, col, 'S')]
    else:
        raise ValueError(f'Unknown direction: {direction}')


def is_valid(point_dir, num_rows, num_cols):
    row, col, direction = point_dir
    return 0 <= row < num_rows and 0 <= col < num_cols


def find_lowest_cost_restriction(matrix, max_len_one_direction=3, min_len_one_direction=0):
    num_rows, num_cols = len(matrix), len(matrix[0])

    def bfs(root, target):
        row, col = root
        cost_table = {}
        queue = [(0, (row, col, 'E', 0))]
        while queue:
            current_cost, (row, col, direction, cnt_dir) = heappop(queue)
            if (row, col, direction, cnt_dir) in cost_table:
                continue
            cost_table[(row, col, direction, cnt_dir)] = current_cost
            node = (row, col, direction)
            neighbors = [neigh for neigh in get_neighbors(node) if is_valid(neigh, num_rows, num_cols)]
            for neighbor in neighbors:
                neigh_row, neigh_col, neigh_dir = neighbor
                if direction == neigh_dir:
                    new_cnt_dir = cnt_dir + 1
                else:
                    new_cnt_dir = 1
                if (
                        new_cnt_dir > max_len_one_direction or
                        (direction != neigh_dir and cnt_dir < min_len_one_direction)
                ):
                    continue
                candidate_cost = current_cost + matrix[neigh_row][neigh_col]
                key = (neigh_row, neigh_col, neigh_dir, new_cnt_dir)
                if cost_table.get(key, float('inf')) <= candidate_cost:
                    continue
                heappush(queue, (candidate_cost, key))

        final_cost = float('inf')
        for (x, y, ori, cnt), cost_val in cost_table.items():
            if (x, y) == (target[0], target[1]):
                final_cost = min(final_cost, cost_val)

        return final_cost

    return bfs((0, 0), (num_rows - 1, num_cols - 1))


if __name__ == '__main__':
    main()
