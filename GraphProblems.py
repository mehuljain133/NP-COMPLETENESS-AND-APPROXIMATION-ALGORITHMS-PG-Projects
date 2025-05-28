# Unit-III Graph Problems: Clique, Vertex Cover, Independent Set, Hamiltonian Cycle Problem, Travelling Salesman Problem, Graph Partitioning, Subgraph problem, Graph Isomorphism, Graph Coloring

import itertools
from collections import defaultdict
import networkx as nx

# CLIQUE (Brute-force)
def is_clique(graph, nodes):
    return all((v in graph[u]) for u, v in itertools.combinations(nodes, 2))

# VERTEX COVER (Check if a set is a cover)
def is_vertex_cover(graph, cover):
    for u in graph:
        for v in graph[u]:
            if u not in cover and v not in cover:
                return False
    return True

# INDEPENDENT SET (no two nodes are connected)
def is_independent_set(graph, nodes):
    return all((v not in graph[u]) for u, v in itertools.combinations(nodes, 2))

# HAMILTONIAN CYCLE (Brute-force)
def has_hamiltonian_cycle(graph):
    nodes = list(graph.keys())
    for perm in itertools.permutations(nodes):
        if all(perm[i+1] in graph[perm[i]] for i in range(len(perm)-1)) and perm[0] in graph[perm[-1]]:
            return True
    return False

# TSP (Brute-force for small graphs)
def tsp_brute_force(graph):
    nodes = list(graph.keys())
    min_path = None
    min_cost = float('inf')
    for perm in itertools.permutations(nodes):
        cost = 0
        valid = True
        for i in range(len(perm) - 1):
            if perm[i+1] in graph[perm[i]]:
                cost += graph[perm[i]][perm[i+1]]
            else:
                valid = False
                break
        if valid and perm[0] in graph[perm[-1]]:
            cost += graph[perm[-1]][perm[0]]
            if cost < min_cost:
                min_cost = cost
                min_path = perm
    return min_path, min_cost

# GRAPH PARTITIONING (2-part partition)
def can_partition(graph):
    color = {}
    def dfs(u, c):
        color[u] = c
        for v in graph[u]:
            if v in color and color[v] == c:
                return False
            if v not in color and not dfs(v, 1 - c):
                return False
        return True
    for node in graph:
        if node not in color and not dfs(node, 0):
            return False
    return True

# SUBGRAPH ISOMORPHISM (Simple check using NetworkX)
def has_subgraph(big_graph, small_graph):
    GM = nx.algorithms.isomorphism.GraphMatcher(big_graph, small_graph)
    return GM.subgraph_is_isomorphic()

# GRAPH ISOMORPHISM
def are_isomorphic(g1, g2):
    return nx.is_isomorphic(g1, g2)

# GRAPH COLORING (k-coloring using backtracking)
def can_color(graph, k):
    nodes = list(graph.keys())
    color = {}

    def assign(i):
        if i == len(nodes):
            return True
        for c in range(1, k+1):
            valid = True
            for neighbor in graph[nodes[i]]:
                if color.get(neighbor) == c:
                    valid = False
                    break
            if valid:
                color[nodes[i]] = c
                if assign(i+1):
                    return True
                del color[nodes[i]]
        return False

    return assign(0)

# Sample usage
if __name__ == "__main__":
    # Undirected graph (adjacency list)
    graph = {
        'A': {'B', 'C'},
        'B': {'A', 'C', 'D'},
        'C': {'A', 'B', 'D'},
        'D': {'B', 'C'},
    }

    print("Clique ['A','B','C']:", is_clique(graph, ['A', 'B', 'C']))
    print("Vertex Cover ['B','C']:", is_vertex_cover(graph, ['B', 'C']))
    print("Independent Set ['A','D']:", is_independent_set(graph, ['A', 'D']))
    print("Has Hamiltonian Cycle:", has_hamiltonian_cycle(graph))
    
    # Weighted complete graph for TSP
    weighted_graph = {
        'A': {'B': 10, 'C': 15, 'D': 20},
        'B': {'A': 10, 'C': 35, 'D': 25},
        'C': {'A': 15, 'B': 35, 'D': 30},
        'D': {'A': 20, 'B': 25, 'C': 30}
    }
    path, cost = tsp_brute_force(weighted_graph)
    print("TSP Path:", path, "Cost:", cost)

    print("Can be 2-partitioned (bipartite):", can_partition(graph))
    print("3-colorable:", can_color(graph, 3))

    # Using NetworkX for subgraph/isomorphism
    G1 = nx.Graph(graph)
    G2 = nx.Graph({'X': {'Y'}, 'Y': {'X'}})
    print("Is Subgraph Isomorphic:", has_subgraph(G1, G2))

    G3 = nx.Graph({'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'A', 'B'}})
    G4 = nx.Graph({'X': {'Y', 'Z'}, 'Y': {'X', 'Z'}, 'Z': {'X', 'Y'}})
    print("Are Graphs Isomorphic:", are_isomorphic(G3, G4))
