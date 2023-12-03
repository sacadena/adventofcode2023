def main():
    with open('data/day03.txt') as h:
        contents = h.readlines()
    matrix = [c.split('\n')[0] for c in contents]
    part_numbers = get_part_numbers(matrix)
    asw1 = sum(part_numbers)
    print(f'(Puzzle 1) Sum part numbers: {asw1}')
    gear_ratios = get_gear_ratios(matrix)
    asw2 = sum(gear_ratios)
    print(f'(Puzzle 2) Sum gear ratios: {asw2}')


def get_neighbor_cells(point, matrix):
    i, j = point
    cells = set()
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if x == 0 and y == 0:
                continue
            if (i + x >= 0) and (i + x < len(matrix)) and (j + y >= 0) and (i + y < len(matrix[0])):
                cells.add((i + x, j + y))
    return cells


def get_gear_ratios(matrix):
    numbers = list(map(str, range(0, 10)))
    ratios = []
    for i, row in enumerate(matrix):
        for j, ch in enumerate(row):
            nums_gear = []
            if ch == '*':
                cells = get_neighbor_cells((i, j), matrix)
                visited = set()
                for cell in cells:
                    if matrix[cell[0]][cell[1]] in numbers and cell not in visited:
                        num, ind_set = gather_number_and_updated_index(cell[1], matrix[cell[0]])
                        nums_gear.append(num)
                        for na in ind_set:
                            visited.add((cell[0], na))
                if len(nums_gear) == 2:
                    ratio = nums_gear[0] * nums_gear[1]
                    ratios.append(ratio)
    return ratios


def get_part_numbers(matrix):
    part_numbers = []
    for i, row in enumerate(matrix):
        j = 0
        while j < len(row):
            row_up = matrix[i-1] if i > 0 else []
            row_down = matrix[i+1] if i < len(matrix) - 1 else []
            if row[j] == '.':
                j += 1
                continue
            if is_symbol_in_neighborhood(j, row, row_up, row_down):
                number, inds_set = gather_number_and_updated_index(j, row)
                part_numbers.append(number)
                j = max(inds_set)
            else:
                j += 1
    return part_numbers


def gather_number_and_updated_index(ind, row):
    numbers = list(map(str, range(0, 10)))
    low = ind
    while row[low] in numbers:
        low -= 1
        if low < 0:
            break

    high = min(ind + 1, len(row) - 1)
    while row[high] in numbers:
        high += 1
        if high >= len(row):
            break
    return int(row[low + 1: high]), set(range(low + 1, high + 1))


def is_char_symbol(char):
    if char not in list(map(str, range(0, 10))) + ['.']:
        return True
    return False


def is_symbol_in_neighborhood(ind, row, row_up, row_down):
    if is_char_symbol(row[ind]):
        return False
    neigh_down = row_down[max(ind - 1, 0): min(ind + 2, len(row_down))]
    neigh_up = row_up[max(ind - 1, 0): min(ind + 2, len(row_up))]
    neigh_row = [row[max(ind - 1, 0)], row[min(ind + 1, len(row_up) - 1)]]
    if any(any(is_char_symbol(n) for n in row_here) for row_here in (neigh_down, neigh_up, neigh_row)):
        return True
    return False


if __name__ == '__main__':
    main()




