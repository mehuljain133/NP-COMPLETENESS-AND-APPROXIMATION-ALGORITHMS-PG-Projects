# Unit-I Introduction to Classes P, NP, NP-Hard, NP Complete: Verifiability and Reduction

import itertools

# Class P: Polynomial-time Algorithm (e.g., Sorting)
def is_sorted(arr):
    """Check if an array is sorted (example of a P problem)"""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i+1]:
            return False
    return True

# Class NP: Verifier for CLIQUE
def verify_clique(graph, k, subset):
    """
    Verifier for the CLIQUE problem.
    Checks if the subset of nodes forms a k-clique in the given graph.
    """
    if len(subset) != k:
        return False
    for u in subset:
        for v in subset:
            if u != v and v not in graph[u]:
                return False
    return True

# NP-Complete: 3-SAT to CLIQUE Reduction (Conceptual Example)
def reduce_3sat_to_clique(cnf_formula):
    """
    Reduces a 3-SAT instance to a graph used for the CLIQUE problem.
    CNF format: List of clauses, each a list of 3 literals (e.g., [['x1', '-x2', 'x3'], ...])
    """
    graph = {}
    node_map = {}
    node_id = 0

    # Create one node for each literal in each clause
    for i, clause in enumerate(cnf_formula):
        for literal in clause:
            node_name = f"{i}_{literal}"
            graph[node_name] = set()
            node_map[node_name] = (i, literal)
            node_id += 1

    # Connect nodes from different clauses if they are not complementary
    for u in graph:
        for v in graph:
            if u != v:
                clause_u, lit_u = node_map[u]
                clause_v, lit_v = node_map[v]
                if clause_u != clause_v and lit_u != negate(lit_v):
                    graph[u].add(v)

    return graph, len(cnf_formula)

def negate(literal):
    """Negate a literal string."""
    if literal.startswith('-'):
        return literal[1:]
    else:
        return '-' + literal

# Example Usage
if __name__ == "__main__":
    print("=== Class P Example ===")
    array = [1, 2, 3, 4]
    print("Is array sorted?", is_sorted(array))

    print("\n=== NP Verifier Example ===")
    # Undirected graph (adjacency list)
    graph = {
        'A': {'B', 'C'},
        'B': {'A', 'C'},
        'C': {'A', 'B'},
        'D': {'E'},
        'E': {'D'}
    }
    subset = ['A', 'B', 'C']
    print("Is subset a 3-clique?", verify_clique(graph, 3, subset))

    print("\n=== 3-SAT to CLIQUE Reduction ===")
    cnf = [['x1', '-x2', 'x3'], ['-x1', 'x2', 'x4'], ['-x3', '-x4', 'x1']]
    clique_graph, k = reduce_3sat_to_clique(cnf)
    print("Graph Nodes:", list(clique_graph.keys()))
    print("k for Clique:", k)
