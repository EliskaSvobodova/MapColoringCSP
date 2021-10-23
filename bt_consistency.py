from copy import deepcopy
from typing import Dict, List, Tuple

from stats import Stats


def color_consistency(nodes: List[str], edges: List[Tuple[str, str]], domain: List[str], stats: Stats):
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
    orig_domain = deepcopy(domains[node])
    for d in domains[node]:
        assigned_nodes[node] = d
        domains[node] = [d]
        stats.steps.append(Stats.Step(deepcopy(assigned_nodes), deepcopy(blank_nodes), deepcopy(domains)))
        if not check_consistency(node, edges, domains):
            assigned_nodes.pop(node)
            domains[node] = orig_domain
            stats.steps.append(Stats.Step(deepcopy(assigned_nodes), deepcopy(blank_nodes), deepcopy(domains)))
            continue
        if color_rec(assigned_nodes, blank_nodes, edges, domains, stats):
            return True
        assigned_nodes.pop(node)
        domains[node] = orig_domain
        stats.steps.append(Stats.Step(deepcopy(assigned_nodes), deepcopy(blank_nodes), deepcopy(domains)))
    blank_nodes.append(node)
    return False


def check_consistency(node: str, edges: Dict[str, List[str]], domains: Dict[str, List[str]]):
    q: List[Tuple[str, str]] = []
    for e in edges[node]:
        q.append((node, e))
    while len(q) > 0:
        node_from, node_to = q.pop(0)
        if update_domain(node_from, node_to, domains):
            if len(domains[node_to]) == 0:
                return False
            for neighbor in edges[node_to]:
                if neighbor != node_from:
                    q.append((node_to, neighbor))
    return True


def update_domain(node_from: str, node_to: str, domains: Dict[str, List[str]]):
    to_remove = []
    for d_to in domains[node_to]:
        satisfactory = [True for d_from in domains[node_from] if d_to != d_from]
        if len(satisfactory) == 0:
            to_remove.append(d_to)
    if len(to_remove) == 0:
        return False
    domains[node_to] = [d for d in domains[node_to] if d not in to_remove]
    return True
