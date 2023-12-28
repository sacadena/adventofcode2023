from collections import defaultdict
from copy import deepcopy
import random


def main():
    with open('data/day25.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    graph = get_graph_list(contents)
    # minimum_cut, subset1, subset2 = karger2(deepcopy(graph))
    minimum_cut, len_subset_1, len_subset_2 = find_minimum_cut(50, graph)
    asw1 = len_subset_1 * len_subset_2
    print(f'(Puzzle 1) Product of cardinality of two disconnected sets: {asw1}')


def karger(graph):
    """ Return the min cut of a graph """
    subsets = defaultdict(set)
    while len(graph) > 2:
        source, target = choose_random_edge(graph)

        graph[source].extend(graph[target])

        subsets[source].update(subsets[target])
        subsets[source].add(target)
        subsets[source].add(source)

        for x in graph[target]:
            graph[x].remove(target)
            graph[x].append(source)
        while source in graph[source]:
            graph[source].remove(source)
        del graph[target]

    length = [len(v) for v in graph.values()]

    keys = list(graph.keys())
    subset1 = subsets[keys[0]]
    subset2 = subsets[keys[1]]
    return length[0], subset1, subset2


def choose_random_edge(graph):
    keys = list(graph.keys())
    source = random.choice(keys)
    target = random.choice(list(graph[source]))
    return source, target


def flood_fill(graph, source):
    seen = set()
    stack = [source]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        for target in graph[node]:
            stack.append(target)
    return seen


def get_graph(lines):
    graph = defaultdict(set)
    for line in lines:
        source, targets = line.split(': ')
        for target in targets.split():
            if source != target:
                graph[source].add(target)
                graph[target].add(source)
    return dict(graph)


def get_graph_list(lines):
    graph = defaultdict(list)
    for line in lines:
        source, targets = line.split(': ')
        for target in targets.split():
            graph[source].append(target)
            graph[target].append(source)
    return graph


def find_minimum_cut(max_iter, graph):
    i = 0
    count = float('inf')
    l1, l2 = len(graph), 0
    while i < max_iter:
        data = deepcopy(graph)
        min_cut, set1, set2 = karger(data)
        if min_cut < count:
            count = min_cut
            l1 = len(set1)
            l2 = len(set2)
        i = i + 1
    return count, l1, l2


if __name__ == '__main__':
    main()
