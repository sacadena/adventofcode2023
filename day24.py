from sympy import symbols, solve


def main():
    with open('data/day24.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]

    initial_positions = [list(map(int, c.split('@')[0].split(','))) for c in contents]
    initial_velocities = [list(map(int, c.split('@')[1].split(','))) for c in contents]
    asw1 = count_eventual_intersections(initial_positions, initial_velocities)
    print(f'(Puzzle 1) Number of intersections: {asw1}')
    positions_velocities = find_initial_positions_and_velocities(initial_positions, initial_velocities)
    asw2 = sum(pos for pos in positions_velocities['positions'])
    print(f'(Puzzle 2) Sum of initial position axes: {asw2}')


def count_eventual_intersections(initial_positions, initial_velocities):
    MIN, MAX = 200000000000000, 400000000000000
    counter = 0
    for i, ((x1, y1, _), (vx1, vy1, _)) in enumerate(zip(initial_positions, initial_velocities)):
        for j, ((x2, y2, _), (vx2, vy2, _)) in enumerate(zip(initial_positions, initial_velocities)):
            if i >= j:
                continue
            if (x1, y1) == (x2, y2) and (vx1, vy1) == (vx2, vy2):
                counter += 1
                continue
            matrix_velocities = [[vx1, -vx2], [vy1, -vy2]]
            bias = [x2 - x1, y2 - y1]
            critical_times = find_critical_times(matrix_velocities, bias)
            if critical_times is None:
                continue
            if (
                    MIN <= (x1 + critical_times[0] * vx1) <= MAX and
                    MIN <= (y2 + critical_times[1] * vy2) <= MAX and
                    all(t >= 0 for t in critical_times)
            ):
                counter += 1
    return counter


def find_initial_positions_and_velocities(initial_positions, initial_velocities):
    x = symbols('x')
    y = symbols('y')
    z = symbols('z')
    vx = symbols('vx')
    vy = symbols('vy')
    vz = symbols('vz')

    (x1, y1, z1), (vx1, vy1, vz1) = initial_positions[0], initial_velocities[0]
    (x2, y2, z2), (vx2, vy2, vz2) = initial_positions[1], initial_velocities[1]
    (x3, y3, z3), (vx3, vy3, vz3) = initial_positions[2], initial_velocities[2]

    sols = solve(
        [(x - x1) * (vy - vy1) - (y - y1) * (vx - vx1), (y - y1) * (vz - vz1) - (z - z1) * (vy - vy1),
         (x - x2) * (vy - vy2) - (y - y2) * (vx - vx2), (y - y2) * (vz - vz2) - (z - z2) * (vy - vy2),
         (x - x3) * (vy - vy3) - (y - y3) * (vx - vx3), (y - y3) * (vz - vz3) - (z - z3) * (vy - vy3)],
        [x, y, z, vx, vy, vz], dict=True)

    s = None
    for s in sols:
        if s[vx] == int(s[vx]) and s[vy] == int(s[vy]) and s[vz] == int(s[vz]):
            break

    return {'positions': (s[x], s[y], s[z]), 'velocities': (s[vx], s[vy], s[vz])}


def find_critical_times(matrix, bias):
    """Solves At = b for t."""
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    assert num_rows == num_cols
    assert num_rows == len(bias)

    if num_rows == 2:
        determinant = compute_2x2_determinant(matrix)
        if determinant == 0:
            return None
        [a, b], [c, d] = matrix
        inverse = [[d / determinant, -b / determinant], [-c / determinant, a / determinant]]
        return dot_product(inverse, bias)
    else:
        raise NotImplementedError


def dot_product(matrix, vector):
    num_cols = len(matrix[0])
    assert num_cols == len(vector)
    return [sum(row[i] * vector[i] for i in range(num_cols)) for row in matrix]


def compute_2x2_determinant(matrix):
    [a, b], [c, d] = matrix
    return a * d - b * c


if __name__ == '__main__':
    main()
