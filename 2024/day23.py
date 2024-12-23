from aocd import get_data, submit
import networkx as nx
from itertools import combinations

data = """kh-tc\nqp-kh\nde-cg\nka-co\nyn-aq\nqp-ub\ncg-tb\nvc-aq\ntb-ka\nwh-tc\nyn-cg\nkh-ub\nta-co\nde-co\ntc-td\ntb-wq\nwh-td\nta-ka\ntd-qp\naq-cg\nwq-ub\nub-vc\nde-ta\nwq-aq\nwq-vc\nwh-yn\nka-de\nkh-ta\nco-tc\nwh-qp\ntb-vc\ntd-yn"""  # Example data
data = get_data(day=23, year=2024)

def parse_data(input):
    G = nx.Graph()
    for line in input.split('\n'):
        comp1, comp2 = line.split('-')
        G.add_edge(comp1, comp2)
    return G

def find_cliques(G):
    return list(nx.find_cliques(G))

def part1(cliques):
    # Get all possible size-3 combinations from cliques of size 3 or larger
    size_3_cliques = set()
    for clique in cliques:
        if len(clique) >= 3:
            for triple in combinations(clique, 3):
                if any(node.startswith('t') for node in triple):
                    size_3_cliques.add(tuple(sorted(triple)))

    return len(size_3_cliques)

def part2(cliques):
    max_clique = max(cliques, key=len)
    return ",".join(sorted(max_clique))

# Process once for both parts
G = parse_data(data)
cliques = find_cliques(G)

print(f"Part 1: {part1(cliques)}")
print(f"Part 2: {part2(cliques)}")