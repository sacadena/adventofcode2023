def main():
    with open('data/day19.txt') as h:
        contents = h.read()
        states, elements = [[na for na in c.split('\n')] for c in contents.split('\n\n')]
        elements = [Element.from_line(el) for el in elements]
        state_map = parse_states(states)
        sum_accepts = get_sum_scores_accepted_elements(elements, state_map)
        asw1 = sum(sum_accepts)
        print(f'(Puzzle 1) Sum of all scores: {asw1}')
        asw2 = total_accepted(state_map)
        print(f'(Puzzle 2) Total possible: {asw2}')


def total_accepted(state_map):
    def dfs(ranges, state):
        if state == "R":
            return 0
        if state == "A":
            product = 1
            for k, (low, high) in ranges.items():
                product *= (high - low + 1)
            return product

        conditions = state_map[state].conditions
        fallback = state_map[state].final_state

        total = 0
        for (variable, comp_type, value, out) in conditions:
            low, high = ranges[variable]

            if comp_type == ">":
                true_lims = (value + 1, high)
                false_lims = (low, value)
            else:
                true_lims = (low, value - 1)
                false_lims = (value, high)

            if true_lims[0] <= true_lims[1]:
                new_ranges = {k: v for k, v in ranges.items()}
                new_ranges[variable] = true_lims
                total += dfs(new_ranges, out)

            if false_lims[0] <= false_lims[1]:
                ranges = {k: v for k, v in ranges.items()}
                ranges[variable] = false_lims
                
        total += dfs(ranges, fallback)
        return total

    initial_ranges = {letter: (1, 4000) for letter in 'xmas'}
    return dfs(initial_ranges, 'in')


def get_sum_scores_accepted_elements(elements, state_map):
    sum_accepts = []
    for el in elements:
        current_state = 'in'
        while True:
            current_cond = state_map[current_state]
            current_state = current_cond.get_new_state(el)
            if current_state == "A":
                sum_accepts.append(el.sum_values())
            if current_state in ("A", "R"):
                break
    return sum_accepts


def parse_states(states):
    out = {}
    for state in states:
        name, rest = state.rstrip('}').split('{')
        out[name] = Conditions.from_line(rest)
    return out


class Conditions:
    def __init__(self, conditions, final_state):
        self.conditions = conditions
        self.final_state = final_state

    @classmethod
    def from_line(cls, line):
        instructions = line.split(',')
        final_state = instructions[-1]

        conditions = []
        for instr in instructions[:-1]:
            comp, out = instr.split(':')
            variable, comp_type, value = comp[0], comp[1], int(comp[2:])
            conditions.append((variable, comp_type, value, out))
        return cls(conditions=conditions, final_state=final_state)

    def get_new_state(self, element):
        comp_type_sign = {'>': 1, '<': -1}
        for (variable, comp_type, value, out) in self.conditions:
            sign = comp_type_sign[comp_type]
            if sign * getattr(element, variable) > sign * value:
                return out
        return self.final_state


class Element:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    @classmethod
    def from_line(cls, line):
        fields = line.lstrip('{').rstrip('}').split(',')
        mapping = {}
        for field in fields:
            name, val = field.split('=')
            mapping[name] = int(val)
        return cls(**mapping)

    def sum_values(self):
        return self.x + self.m + self.a + self.s


if __name__ == "__main__":
    main()