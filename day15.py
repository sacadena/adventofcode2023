from collections import defaultdict


def main():
    with open('data/day15.txt') as h:
        contents = h.read()

    steps = contents.split(',')

    asw1 = sum([compute_hash(step) for step in steps])
    print(f'(Puzzle 1) Sum hashes: {asw1}')
    parsed_steps = [get_label_and_operation(step) for step in steps]
    boxes = get_boxes_state(parsed_steps)
    asw2 = get_total_score(boxes)
    print(f'(Puzzle 2) Total score: {asw2}')


def get_total_score(boxes):
    total_score = 0
    for ind, lenses in boxes.items():
        for slot, lens in enumerate(lenses):
            total_score += (ind + 1) * (slot + 1) * lens[1]
    return total_score


def get_boxes_state(parsed_steps):
    boxes = defaultdict(list)
    for step in parsed_steps:
        label, operation, power = step
        box_ind = str(compute_hash(label))
        if operation == '-' and box_ind in boxes:
            lenses = boxes[box_ind]
            for lens in lenses:
                if lens[0] == label:
                    lenses.remove(lens)
                    break
        if operation == '=':
            if box_ind in boxes:
                existing = False
                for lens in boxes[box_ind]:
                    if lens[0] == label:
                        lens[1] = power
                        existing = True
                        break
                if not existing:
                    boxes[box_ind].append([label, power])
            else:
                boxes[box_ind].append([label, power])

    return {int(k): v for k, v in boxes.items() if v}


def compute_hash(string):
    current_value = 0
    for ch in string:
        current_value += ord(ch)
        current_value *= 17
    return current_value % 256


def get_label_and_operation(string):
    if string.endswith('-'):
        return string[:-1], '-', None
    label, power = string.split('=')
    return label, '=', int(power)


if __name__ == '__main__':
    main()
