from copy import deepcopy
from typing import Dict, List, Tuple

from stats import Stats


def color_bt_filtering(nodes: List[str], edges: List[Tuple[str, str]], domain: List[str], stats: Stats):
    col_nodes = {}
    blank_nodes = deepcopy(nodes)
    edges_dict = {n: [] for n in nodes}
    for e in edges:
        edges_dict[e[0]].append(e[1])
        edges_dict[e[1]].append(e[0])
    domain_dict = {n: deepcopy(domain) for n in nodes}
    if color_rec(col_nodes, blank_nodes, edges_dict, domain_dict, stats):
        return col_nodes
    return None


def color_rec(assigned_nodes: Dict[str, str], blank_nodes: List[str], edges: Dict[str, List[str]], domains: Dict[str, List[str]], stats: Stats):
    if len(blank_nodes) == 0:
        return True
    node = blank_nodes.pop()
    for d in domains[node]:
        assigned_nodes[node] = d
        orig_domain = deepcopy(domains)
        for neighbor in edges[node]:
            if d in domains[neighbor]:
                domains[neighbor].remove(d)
        stats.steps.append(Stats.Step(deepcopy(assigned_nodes), deepcopy(blank_nodes), deepcopy(domains)))
        if not check_domains(node, edges, domains):
            assigned_nodes.pop(node)
            domains = orig_domain
            stats.steps.append(Stats.Step(deepcopy(assigned_nodes), deepcopy(blank_nodes), deepcopy(domains)))
            continue
        if color_rec(assigned_nodes, blank_nodes, edges, domains, stats):
            return True
        assigned_nodes.pop(node)
        domains = orig_domain
        stats.steps.append(Stats.Step(deepcopy(assigned_nodes), deepcopy(blank_nodes), deepcopy(domains)))
    blank_nodes.append(node)
    return False


def check_domains(node: str, edges: Dict[str, List[str]], domains: Dict[str, List[str]]):
    for neighbor in edges[node]:
        if len(domains[neighbor]) == 0:
            return False
    return True
