def main():
    with open('data/day12.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    rows = [c.split()[0] for c in contents]
    counts_damaged_groups = [list(map(int, c.split()[1].split(','))) for c in contents]
    number_of_ways = [count_num_ways_dp(row, counts) for row, counts in zip(rows, counts_damaged_groups)]
    asw1 = sum(number_of_ways)
    print(f'(Puzzle 1) Total arrangements: {asw1}')
    rows, counts_damaged_groups = unfold(rows, counts_damaged_groups, 5)
    number_of_ways = [count_num_ways_dp(row, counts) for row, counts in zip(rows, counts_damaged_groups)]
    asw2 = sum(number_of_ways)
    print(f'(Puzzle 2) Total arrangements: {asw2}')


def unfold(rows, counts_damaged_groups, times):
    new_rows, new_counts = [], []
    for row, counts in zip(rows, counts_damaged_groups):
        new_rows.append('?'.join(row for _ in range(times)))
        new_counts.append(counts * times)
    return new_rows, new_counts


def insert_in_string(string, ind, character):
    s = list(string)
    s[ind] = character
    return ''.join(s)


def count_num_ways_dp(line, counts):
    dp_table = {}

    def dfs(i, ic, current_len):
        key = (i, ic, current_len)
        if key in dp_table:
            return dp_table[key]
        if i >= len(line):
            if ic == len(counts) and current_len == 0:
                return 1
            if ic == (len(counts) - 1) and counts[ic] == current_len:
                return 1
            return 0
        out = 0
        for c in ('.', '#'):
            if line[i] in (c, '?'):
                if c == '.' and current_len == 0:
                    out += dfs(i + 1, ic, current_len)
                elif c == '.' and (current_len > 0) and (ic < len(counts)) and counts[ic] == current_len:
                    out += dfs(i + 1, ic + 1, 0)
                elif c == '#':
                    out += dfs(i + 1, ic, current_len + 1)
        dp_table[key] = out
        return out
    return dfs(0, 0, 0)


def count_num_ways_naive(line, counts):
    def dfs(ind, state, inds_unknown):
        if ind >= len(inds_unknown):
            return int(is_valid(state, counts))
        line_ind = inds_unknown[ind]
        n_dot = dfs(ind + 1, insert_in_string(state, line_ind, '.'), inds_unknown)
        n_hashtag = dfs(ind + 1, insert_in_string(state, line_ind, '#'), inds_unknown)
        return n_dot + n_hashtag

    unknown = [i for i, val in enumerate(line) if val == "?"]
    return dfs(0, line, unknown)


def is_valid(line, counts):
    islands = [s for s in line.split('.') if s]
    if len(islands) != len(counts):
        return False
    return all(len(island) == count for island, count in zip(islands, counts))


if __name__ == '__main__':
    main()
