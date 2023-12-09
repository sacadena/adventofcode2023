def main():
    with open('data/day09.txt') as h:
        contents = h.readlines()
    reports = [list(map(int, c.split())) for c in contents]
    next_elements = [find_next_element(report) for report in reports]
    asw1 = sum(next_elements)
    print(f'(Puzzle 1) Sum last next elements: {asw1}')
    previous_elements = [find_previous_element(report) for report in reports]
    asw2 = sum(previous_elements)
    print(f'(Puzzle 2) Sum of previous elements: {asw2}')


def find_next_element(report):
    diffs = compute_all_diffs(report)
    diffs_reversed = diffs[::-1]
    for i, diff in enumerate(diffs_reversed):
        if i == 0:
            diff.append(0)
        else:
            diff.append(diff[-1] + diffs_reversed[i - 1][-1])
    return diffs_reversed[-1][-1]


def find_previous_element(report):
    diffs = compute_all_diffs(report)
    diffs_reversed = diffs[::-1]
    for i, diff in enumerate(diffs_reversed):
        if i == 0:
            diff.insert(0, 0)
        else:
            diff.insert(0, diff[0] - diffs_reversed[i - 1][0])
    return diffs_reversed[-1][0]


def compute_all_diffs(report):
    row = report
    diffs = [row]
    while not all([el == 0 for el in row]):
        row = get_diff_row(row)
        diffs.append(row)
    return diffs


def get_diff_row(row):
    return [
        l2 - l1 for l1, l2 in zip(row, row[1:])
    ]


if __name__ == "__main__":
    main()
