# Unit-V Techniques to design approximation algorithms: LP-rounding, Primal-Dual, Dual Fitting, Greedy, Local Search.

import numpy as np
from scipy.optimize import linprog
import random

# 1. Greedy Set Cover Approximation
def greedy_set_cover(universe, subsets):
    uncovered = set(universe)
    cover = []
    while uncovered:
        best_set = max(subsets, key=lambda s: len(uncovered & s))
        cover.append(best_set)
        uncovered -= best_set
    return cover

# 2. Local Search for Max Cut Approximation
def local_search_max_cut(graph):
    # graph: adjacency list with weights, e.g., {u: {v: w, ...}, ...}
    nodes = list(graph.keys())
    partition = set(random.sample(nodes, len(nodes)//2))  # initial random partition

    improved = True
    while improved:
        improved = False
        for node in nodes:
            current_side = node in partition
            gain = 0
            for neighbor, w in graph[node].items():
                if (neighbor in partition) != current_side:
                    gain += w
                else:
                    gain -= w
            if gain > 0:
                if current_side:
                    partition.remove(node)
                else:
                    partition.add(node)
                improved = True
    return partition

# 3. LP Rounding for Vertex Cover
def lp_rounding_vertex_cover(edges, num_vertices):
    # Formulate LP:
    # Minimize sum x_i subject to x_u + x_v >= 1 for all edges (u,v)
    # 0 <= x_i <= 1 for all i
    c = np.ones(num_vertices)
    A = []
    b = []
    for u, v in edges:
        row = np.zeros(num_vertices)
        row[u] = 1
        row[v] = 1
        A.append(row)
        b.append(1)
    bounds = [(0, 1)] * num_vertices

    res = linprog(c, A_ub=-np.array(A), b_ub=-np.array(b), bounds=bounds, method='highs')

    # Rounding
    x = res.x
    cover = [i for i in range(num_vertices) if x[i] >= 0.5]
    return cover

# 4. Primal-Dual Approximation for Vertex Cover
def primal_dual_vertex_cover(edges, num_vertices):
    uncovered_edges = set(edges)
    cover = set()
    dual = [0] * len(edges)

    while uncovered_edges:
        e = uncovered_edges.pop()
        u, v = e
        # Increase dual variable for edge e
        dual_val = 1
        # Add both endpoints to cover if not already in
        if u not in cover:
            cover.add(u)
        if v not in cover:
            cover.add(v)
        # Remove all edges covered by these nodes
        uncovered_edges = {edge for edge in uncovered_edges if edge[0] not in cover and edge[1] not in cover}
    return list(cover)

# 5. Dual Fitting (conceptual)
def dual_fitting_vertex_cover(edges, num_vertices):
    # Start with zero dual variables
    dual = [0] * num_vertices
    cover = set()
    for u, v in edges:
        # Increase dual variables greedily
        if u not in cover and v not in cover:
            dual[u] += 1
            dual[v] += 1
            cover.add(u)
            cover.add(v)
    return list(cover)

# === Sample usage ===
if __name__ == "__main__":
    print("=== Greedy Set Cover Approximation ===")
    universe = set(range(1, 7))
    subsets = [{1,2,3}, {2,4}, {3,4,5}, {5,6}]
    cover = greedy_set_cover(universe, subsets)
    print("Cover sets:", cover)

    print("\n=== Local Search Max Cut Approximation ===")
    graph = {
        0: {1:1, 2:1},
        1: {0:1, 2:1},
        2: {0:1, 1:1, 3:1},
        3: {2:1}
    }
    part = local_search_max_cut(graph)
    print("Partition:", part)

    print("\n=== LP Rounding for Vertex Cover ===")
    edges = [(0,1), (1,2), (2,3), (3,0)]
    num_vertices = 4
    cover = lp_rounding_vertex_cover(edges, num_vertices)
    print("Vertex cover:", cover)

    print("\n=== Primal-Dual Approximation for Vertex Cover ===")
    cover = primal_dual_vertex_cover(edges, num_vertices)
    print("Vertex cover:", cover)

    print("\n=== Dual Fitting Approximation for Vertex Cover ===")
    cover = dual_fitting_vertex_cover(edges, num_vertices)
    print("Vertex cover:", cover)
