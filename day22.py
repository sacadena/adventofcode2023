from copy import deepcopy


def main():
    with open('data/day22.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    bricks = [Brick.from_line(c) for c in contents]
    updated_bricks = update_bricks_after_fall(bricks)

    asw1, asw2 = solve(updated_bricks)
    print(f'(Puzzle 1) Number of bricks that can be disintegrated: {asw1}')
    print(f'(Puzzle 2) Total of moved bricks: {asw2}')


def solve(bricks):
    occupied_cubes = set()
    for brick in bricks:
        for cube in brick.cubes:
            occupied_cubes.add(cube)

    previous_occupied_cubes = deepcopy(occupied_cubes)
    previous_bricks = deepcopy(bricks)
    num_can_fall_once = 0
    num_will_fall_in_total = 0
    for i, brick in enumerate(bricks):
        occupied_cubes = deepcopy(previous_occupied_cubes)
        bricks = deepcopy(previous_bricks)

        for (x, y, z) in brick.cubes:
            occupied_cubes.discard((x, y, z))

        fallen_bricks = set()
        while True:
            something_moved = False
            for other_brick in bricks:
                if other_brick == brick:
                    continue
                is_brick_moved = True
                for (x, y, z) in other_brick.cubes:
                    if z == 1:
                        is_brick_moved = False
                    if (x, y, z - 1) in occupied_cubes and (x, y, z - 1) not in other_brick.cubes:
                        is_brick_moved = False
                if is_brick_moved:
                    fallen_bricks.add(other_brick)
                    for (x, y, z) in other_brick.cubes:
                        assert (x, y, z) in occupied_cubes
                        occupied_cubes.discard((x, y, z))
                        occupied_cubes.add((x, y, z - 1))
                    brick.set_new_cubes([(x, y, z - 1) for (x, y, z) in other_brick.cubes])
                    something_moved = True
            if not something_moved:
                break
        if len(fallen_bricks) == 0:
            num_can_fall_once += 1
        num_will_fall_in_total += len(fallen_bricks)

    return num_can_fall_once, num_will_fall_in_total


def update_bricks_after_fall(bricks):
    occupied_cubes = set()
    for brick in bricks:
        for cube in brick.cubes:
            occupied_cubes.add(cube)

    while True:
        something_moved = False
        for brick in bricks:
            is_brick_moved = True
            for (x, y, z) in brick.cubes:
                if z == 1:
                    is_brick_moved = False
                if (x, y, z - 1) in occupied_cubes and (x, y, z - 1) not in brick.cubes:
                    is_brick_moved = False

            if is_brick_moved:
                something_moved = True
                for (x, y, z) in brick.cubes:
                    assert (x, y, z) in occupied_cubes
                    occupied_cubes.discard((x, y, z))
                    occupied_cubes.add((x, y, z - 1))
                brick.set_new_cubes([(x, y, z - 1) for (x, y, z) in brick.cubes])

        if not something_moved:
            break
    return bricks


class Brick:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

    @classmethod
    def from_line(cls, line):
        p1, p2 = line.split('~')
        x1, y1, z1 = [int(c) for c in p1.split(',')]
        x2, y2, z2 = [int(c) for c in p2.split(',')]
        return cls(x1, y1, z1, x2, y2, z2)

    @property
    def axis(self):
        x1, y1, z1 = self.x1, self.y1, self.z1
        x2, y2, z2 = self.x2, self.y2, self.z2
        for ax1, ax2, name in zip((x1, y1, z1), (x2, y2, z2), ('x', 'y', 'z')):
            if ax1 != ax2:
                return name
        return 'all'

    @property
    def cubes(self):

        x1, y1, z1 = self.x1, self.y1, self.z1

        if self.axis == 'all':
            return [(x1, y1, z1)]

        if self.axis == 'x':
            return [(x, y1, z1) for x in range(x1, self.x2 + 1)]

        if self.axis == 'y':
            return [(x1, y, z1) for y in range(y1, self.y2 + 1)]

        if self.axis == 'z':
            return [(x1, y1, z) for z in range(z1, self.z2 + 1)]

    def set_new_cubes(self, new_cubes):
        self.x1, self.y1, self.z1 = new_cubes[0]
        self.x2, self.y2, self.z2 = new_cubes[-1]
        return

    def __repr__(self):
        return f'Brick(({self.x1}, {self.y1}, {self.z1}), ({self.x2}, {self.y2}, {self.z2}))'


if __name__ == "__main__":
    main()
