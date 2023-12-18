def main():
    with open('data/day18.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    instructions = list(
        map(lambda x: (x[0], int(x[1]), x[2].lstrip('(').rstrip(')')), [c.split() for c in contents])
    )
    # Less efficient solution:
    # boundary = obtain_boundary(instructions)
    # area = find_area(boundary)
    # asw1 = len(boundary) + area

    # Using shoelace formula
    asw1 = find_area_efficient(instructions)
    print(f'(Puzzle 1) Total area: {asw1}')
    instructions = update_instructions(instructions)
    asw2 = find_area_efficient(instructions)
    print(f'(Puzzle 2) Total area: {asw2}')


def find_area_efficient(instructions):
    x, y = (0, 0)
    directions = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}
    perimeter = 0
    points = [(x, y)]
    for instr in instructions:
        dir_, distance = instr[0], instr[1]
        perimeter += distance
        dx, dy = directions[dir_]
        x, y = x + distance * dx, y + distance * dy
        points.append((x, y))

    area = 0
    for (x1, y1), (x2, y2) in zip(points[:-1], points[1:]):
        area += (x1 * y2 - x2 * y1)  # shoelace formula
    return abs(area // 2) + perimeter//2 + 1


def update_instructions(instructions):
    new_instructions = []
    dirs = ['R', 'D', 'L', 'U']
    for inst in instructions:
        distance = int(inst[2].lstrip('#')[:5], 16)
        ori = dirs[int(inst[2][-1])]
        new_instructions.append((ori, distance))
    return new_instructions


def find_area(boundary):
    minx = min(b[0] for b in boundary)
    maxx = max(b[0] for b in boundary)
    miny = min(b[1] for b in boundary)
    maxy = max(b[1] for b in boundary)

    start_node = None, None
    for b in boundary:
        if minx <= b[0] < maxx and miny <= b[1] < maxy:
            if (b[0] + 1, b[1] + 1) not in boundary:
                start_node = (b[0] + 1, b[1] + 1)
                break

    visited = set(start_node)
    stack = [start_node]
    s = 0

    while stack:
        node = stack.pop()
        x, y = node
        if x < minx or y < miny or y >= maxy or x >= maxx or node in boundary or node in visited:
            continue

        visited.add(node)
        s += 1
        dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        for dx, dy in dirs:
            neighbor = (x + dx, y + dy)
            stack.append(neighbor)

    return s


def obtain_boundary(steps):
    x, y = 0, 0
    boundary = []
    directions = {'U': [-1, 0], 'D': [1, 0], 'R': [0, 1], 'L': [0, -1]}
    for step in steps:
        dir_, n = step[0], step[1]
        dx, dy = directions[dir_]
        for _ in range(1, n + 1):
            x, y = x + dx, y + dy
            boundary.append((x, y))
    return boundary


if __name__ == "__main__":
    main()
