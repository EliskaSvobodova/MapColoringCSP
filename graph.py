import random
from copy import deepcopy
from typing import List, Tuple, Dict


class Node:
    def __init__(self, name, domain, value=None):
        self.name = name
        self.domain = domain
        self.value = value


class TreeNode(Node):
    def __init__(self, name, domain, value=None):
        super().__init__(name, domain, value)
        self.sons = []


class Edge:
    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2


class TreeGraph:
    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]], domain: List[str]):
        nodes = {n: TreeNode(n, deepcopy(domain)) for n in nodes}
        self.root = random.choice(list(nodes.values()))
        nodes.pop(self.root.name)
        self.init_from_root(self.root, nodes, edges)

    def init_from_root(self, node: TreeNode, nodes: Dict[str, TreeNode], edges: List[Tuple[str, str]]):
        for e in edges:
            if e[0] == node.name:
                node.sons.append(nodes[e[1]])
                nodes.pop(e[1])
                edges.remove(e)
            elif e[1] == node.name:
                node.sons.append(nodes[e[0]])
                nodes.pop(e[0])
                edges.remove(e)
        for s in node.sons:
            nodes, edges = self.init_from_root(s, nodes, edges)
        return nodes, edges

    def color_recursion(self, node: TreeNode):
        pass


class Graph:
    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]], domain: List[str]):
        self.nodes = {n: Node(n, domain, None) for n in nodes}
        self.edges = [Edge(self.nodes[e[0]], self.nodes[e[1]]) for e in edges]

    def color(self):
        col_nodes = {}

        self.color_rec()

    def color_rec(self, col_nodes: Dict[str, str], blank_nodes: List[str], edges: Dict[str, List[str]], domain: List[str]):
        if len(blank_nodes) == 0:
            return True
        node = blank_nodes.pop()
        for color in domain:
            success = True
            for neighbor in edges[node]:
                if neighbor in col_nodes and col_nodes[neighbor] == color:
                    success = False
                    break
            if success:
                col_nodes[node] = color
                if self.color_rec(col_nodes, blank_nodes, edges, domain):
                    return True
                col_nodes.pop(node)
        return False
