def main():
    with open('data/day05.txt') as h:
        contents = h.read()
    groups = contents.split('\n\n')
    groups = [g.split('\n') for g in groups]
    seeds = parse_seeds_one(groups[0][0])
    mappings = get_mappings(groups[1:])
    locations = [get_final_locations(seed, mappings) for seed in seeds]
    asw1 = min(locations)
    print(f'(Puzzle 1) Min location: {asw1}')
    critical_seed_points = identify_critical_points(groups)
    seed_ranges = parse_seeds_two(groups[0][0])
    min_locations = [
        find_minimum_location(seed_range, critical_seed_points, mappings)
        for seed_range in seed_ranges
    ]
    asw2 = min(min_locations)
    print(f'(Puzzle 2) Min location: {asw2}')


def find_minimum_location(seed_range, critical_seed_points, mappings):
    start, end = seed_range
    critical_here = [c for c in critical_seed_points if (start <= c < end)]
    critical_here.insert(0, start)
    critical_here.insert(-1, end)
    locations_here = [get_final_locations(seed, mappings) for seed in critical_here]
    return min(locations_here)


def get_final_locations(seed, mappings):
    transformed = seed
    key = 'seed'
    while key in mappings:
        key, func = mappings[key]
        transformed = func(transformed)
    return transformed


def parse_seeds_one(line):
    return list(map(int, line.lstrip("seed: ").split()))


def identify_critical_points(groups):
    transformed_critical_points = []
    for group in groups[1:][::-1]:
        s, t, instructions = get_instructions(group)
        critical_input_points_here = []
        for instr in instructions:
            critical_input_points_here.extend([instr[1], instr[1] + instr[2]])
        critical_input_points_here.insert(0, 0)
        critical_input_points_here = list(set(critical_input_points_here))
        inv_func = inv_function_generator(instructions)
        transformed_critical_points = [inv_func(c) for c in transformed_critical_points]
        transformed_critical_points.extend(critical_input_points_here)

    return sorted(set(transformed_critical_points))


def parse_seeds_two(line):
    initial_seeds = list(map(int, line.lstrip("seed: ").split()))
    seed_ranges = []
    for ind in range(0, len(initial_seeds), 2):
        new = (initial_seeds[ind], initial_seeds[ind] + initial_seeds[ind + 1])
        seed_ranges.append(new)
    return seed_ranges


def get_mappings(groups):
    mappings = {}
    for g in groups:
        mappings.update(get_mapping_group(g))
    return mappings


def get_mapping_group(group):
    source, target, instructions = get_instructions(group)
    func = function_generator(instructions)
    return {source: (target, func)}


def get_instructions(group):
    source, target = group[0].rstrip(" map:").split("-to-")
    return source, target, [list(map(int, line.split())) for line in group[1:]]


def function_generator(instructions):
    def func(arg):
        for inst in instructions:
            output = parse_instruction(inst, arg)
            if output is not None:
                return output
        return arg
    return func


def parse_instruction(instruction, number):
    destination, source, delta = instruction
    if (number >= source) and (number < source + delta):
        return number - source + destination
    return None


def inv_parse_instruction(instruction, number):
    destination, source, delta = instruction
    if (number >= destination) and (number < destination + delta):
        return number - destination + source
    return None


def inv_function_generator(instructions):
    def func(arg):
        for inst in instructions:
            output = inv_parse_instruction(inst, arg)
            if output is not None:
                return output
        return arg
    return func


if __name__ == "__main__":
    main()
