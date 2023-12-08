import math
from collections import defaultdict


def main():
    with open('data/day08.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    instructions = contents[0]
    graph = parse_graph(contents[2:])
    asw1 = count_steps(instructions, graph)
    print(f'(Puzzle 1) Number of steps: {asw1}')
    asw2 = count_simultaneous_steps(instructions, graph)
    print(f'(Puzzle 2) Number of steps: {asw2}')


def count_simultaneous_steps(instructions, graph):
    starts_ending = 'A'
    targets_ending = 'Z'
    start_nodes = [
        node for node in graph if node.endswith(starts_ending)
    ]
    end_nodes = [
        node for node in graph if node.endswith(targets_ending)
    ]

    num_steps_starts_ends = defaultdict(list)
    for start in start_nodes:
        for end in end_nodes:
            num_steps = count_steps(instructions, graph, start, end)
            num_steps_starts_ends[start].append((end, num_steps))

    min_steps = []
    for list_end_steps in num_steps_starts_ends.values():
        min_steps.append(
            min(list_end_steps, key=lambda x: x[1] if x[1] is not None else math.inf)
        )
    return math.lcm(*[x[1] for x in min_steps])


def count_simultaneous_steps_naive(instructions, graph):
    starts_ending = 'A'
    targets_ending = 'Z'
    current_nodes = [
        node for node in graph if node.endswith(starts_ending)
    ]
    i = 0
    num_steps = 0
    while not(all(current.endswith(targets_ending) for current in current_nodes)):
        num_steps += 1
        current_nodes = [graph[current][instructions[i]] for current in current_nodes]
        i = (i + 1) % len(instructions)
    return num_steps


def count_steps(instructions, graph, start="AAA", end="ZZZ"):
    current = start
    i = 0
    num_steps = 0
    visited_edges = set()
    while current != end:
        num_steps += 1
        previous = current
        current = graph[previous][instructions[i]]
        i = (i + 1) % len(instructions)
        if (previous, current, i) in visited_edges:
            return None
        visited_edges.add((previous, current, i))
    return num_steps


def parse_graph(contents):
    graph = {}
    for line in contents:
        source, targets = line.split(" = ")
        targets = targets.lstrip('(').rstrip(')').split(', ')
        graph[source] = {'R': targets[1], 'L': targets[0]}
    return graph


if __name__ == "__main__":
    main()

