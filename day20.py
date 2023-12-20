from collections import deque, defaultdict, Counter
from typing import Optional
from math import gcd


def main():
    with open('data/day20.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    module_map = get_reset_module_map(contents)
    counter = Counter({False: 0, True: 0})
    for _ in range(1000):
        counter += state_counts_after_pressed_button(module_map)
    asw1 = counter[False] * counter[True]
    print(f'(Puzzle 1) Number of pulses sent: {asw1}')
    module_map = get_reset_module_map(contents)
    predecessors = find_predecessors(module_map, 'rx')
    frequencies_predecessors = find_number_of_cycles_to_reach_states(
        module_map, predecessors)
    asw2 = least_common_multiple(frequencies_predecessors)
    print(f'(Puzzle 2) Number of button presses for low to reach state rx: {asw2}')


def get_reset_module_map(contents):
    modules = [Module.from_line(c) for c in contents]
    module_map = {m.name: m for m in modules}
    return initialize_conjunction_moduels(module_map)


def find_predecessors(module_map, state):
    inverted_module_map = defaultdict(list)
    for name, module in module_map.items():
        for dest in module.destinations:
            inverted_module_map[dest].append(module.name)
    return inverted_module_map[inverted_module_map[state][0]]


def find_number_of_cycles_to_reach_states(module_map, states):

    previous = {}
    to_lcm = []
    count_per_module = defaultdict(int)

    def _push_button(map, current_press_number):
        queue = deque([(map['broadcaster'], ('button', False))])
        while queue:
            current_module, (input_name, message) = queue.popleft()

            if not message:  # Only relevant for puzzle 2
                name = current_module.name
                if name in previous and count_per_module[name] == 2 and name in states:
                    to_lcm.append(current_press_number - previous[name])
                previous[name] = current_press_number
                count_per_module[name] += 1

            message = current_module.output(message)
            if message is None:
                continue
            for destination in current_module.destinations:
                if destination not in map:
                    continue
                dest_module = map[destination]
                if dest_module.type == '&':
                    dest_module.state[current_module.name] = message
                queue.append((dest_module, (current_module.name, message)))
        return

    for press in range(1, int(1e10)):
        _push_button(module_map, current_press_number=press)
        if len(to_lcm) == len(states):
            break
    return to_lcm


def initialize_conjunction_moduels(module_map):
    for name, module in module_map.items():
        for dest in module.destinations:
            if dest in module_map and module_map[dest].type == '&':
                module_map[dest].state[name] = False
    return module_map


def least_common_multiple(numbers):
    lcm = numbers[0]
    for i in numbers[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def state_counts_after_pressed_button(module_map):

    queue = deque([(module_map['broadcaster'], ('button', False))])
    count = {False: 0, True: 0}
    while queue:
        current_module, (input_name, message) = queue.popleft()
        # print(f"{input_name} -{'high' if message else 'low'}-> {current_module.name}")
        count[message] += 1
        message = current_module.output(message)
        if message is None:
            continue
        for destination in current_module.destinations:
            if destination not in module_map:
                count[message] += 1
                # print(f"{current_module.name} -{'high' if message else 'low'}-> {destination}")
                continue
            dest_module = module_map[destination]
            if dest_module.type == '&':
                dest_module.state[current_module.name] = message
            queue.append((dest_module, (current_module.name, message)))

    return count


class Module:
    def __init__(self, name, type, destinations, state):
        self.name = name
        self.type = type
        self.destinations = destinations
        self.state = state

    @classmethod
    def from_line(cls, line):
        source, destinations = line.split(' -> ')
        destinations = destinations.split(', ')
        if source == 'broadcaster':
            return cls(name=source, type='broadcaster', destinations=destinations, state=True)
        type, name = source[0], source[1:]
        if type == '&':
            return cls(name=name, type=type, destinations=destinations, state={})
        return cls(name=name, type=type, destinations=destinations, state=False)

    def output(self, input_: bool) -> Optional[bool]:
        if self.type == 'broadcaster':
            return input_
        if self.type == '%':
            if input_:
                return None
            else:
                self.state = not self.state
                return self.state
        if self.type == '&':
            if all(self.state.values()):
                return False
            return True

    def __repr__(self):
        return f'Module(name={self.name}, type={self.type}, destinations={self.destinations}, state={self.state})'


if __name__ == '__main__':
    main()
