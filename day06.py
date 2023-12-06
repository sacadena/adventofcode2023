def main():
    with open('data/day06.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    times, previous_distances = parse_contents_one(contents)
    num_better_distances = find_better_distances(times, previous_distances)
    asw1 = prod(num_better_distances)
    print(f'(Puzzle 1) Product of number of record passing: {asw1}')
    times, previous_distances = parse_contents_two(contents)
    # probably there's more efficient way by finding intercepts of parabola
    # but this ran fast enough:
    asw2 = find_better_distances(times, previous_distances)[0]
    print(f'(Puzzle 2) Number of record passing: {asw2}')


def parse_contents_two(contents):
    time = int(''.join(contents[0].lstrip("Time: ").split()))
    prev_distance = int(''.join(contents[1].lstrip("Distance: ").split()))
    return [time], [prev_distance]


def find_better_distances(times, previous_distances):
    base_speed = 1
    num_better_distances = []
    for time, prev_distance in zip(times, previous_distances):
        distances = [(time - time_pressed) * (base_speed * time_pressed) for time_pressed in range(time + 1)]
        num_better_distances.append(len([d for d in distances if d > prev_distance]))
    return num_better_distances


def parse_contents_one(contents):
    times = list(map(int, contents[0].lstrip("Time: ").split()))
    previous_distances = list(map(int, contents[1].lstrip("Distance: ").split()))
    return times, previous_distances


def prod(array):
    out = 1
    for a in array:
        out *= a
    return out


if __name__ == "__main__":
    main()