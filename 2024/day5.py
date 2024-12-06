from aocd import get_data, submit
from functools import cmp_to_key

# data = "47|53\n97|13\n97|61\n97|47\n75|29\n61|13\n75|53\n29|13\n97|29\n53|29\n61|53\n97|53\n61|29\n47|13\n75|47\n97|75\n47|61\n75|61\n47|29\n75|13\n53|13\n\n75,47,61,53,29\n97,61,53,29,13\n75,29,13\n75,97,47,61,53\n61,13,29\n97,13,75,29,47"
data = get_data(day=5, year=2024)

def parse_input(input):
    rules = {}
    updates = []

    rules_raw, updates_raw = input.split('\n\n')
    for line in rules_raw.split('\n'):
        before, after = map(int, line.split('|'))
        if before not in rules:
            rules[before] = []
        rules[before].append(after)

    for line in updates_raw.split('\n'):
        updates.append(list(map(int, line.split(','))))

    return rules, updates

def compare_pages(a, b, rules):
    if a == b:
        return 0
    if a in rules and b in rules[a]:
        return -1
    if b in rules and a in rules[b]:
        return 1
    return 0

def sort_update(update, rules):
    sorted_update = sorted(update, key=cmp_to_key(lambda x, y: compare_pages(x, y, rules)))
    return sorted_update

rules, updates = parse_input(data)
sorted_updates = [sort_update(update, rules) for update in updates]

middle_sum_valid = 0
middle_sum_invalid = 0

for update, sorted_update in zip(updates, sorted_updates):

    if update != sorted_update:
        middle_sum_invalid += sorted_update[len(sorted_update) // 2]
    else:
        middle_sum_valid += update[len(update) // 2]

print(f"Part 1: {middle_sum_valid}")
print(f"Part 2: {middle_sum_invalid}")