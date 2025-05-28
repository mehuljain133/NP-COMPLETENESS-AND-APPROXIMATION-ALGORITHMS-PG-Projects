# Unit-II Proving NP-Completeness from first principle: Satisfiability Problem (SAT), 3SAT

import itertools

# SAT verifier
def is_satisfiable(clauses, assignment):
    """
    Verifies if the boolean assignment satisfies the CNF formula.
    clauses: list of clauses, e.g., [['x1', '-x2'], ['x2', 'x3']]
    assignment: dict mapping variable names to boolean values
    """
    for clause in clauses:
        clause_satisfied = False
        for literal in clause:
            var = literal.lstrip('-')
            value = assignment.get(var, False)
            if literal.startswith('-'):
                value = not value
            clause_satisfied |= value
        if not clause_satisfied:
            return False
    return True

# Generate all possible assignments for n variables
def generate_assignments(variables):
    """
    Generates all possible True/False assignments for a list of variables.
    """
    for values in itertools.product([True, False], repeat=len(variables)):
        yield dict(zip(variables, values))

# Solve SAT by brute-force (to illustrate the idea of verifiability)
def solve_sat(clauses):
    """
    Solves the SAT problem by checking all truth assignments.
    Returns a satisfying assignment if one exists.
    """
    variables = sorted({literal.strip('-') for clause in clauses for literal in clause})
    for assignment in generate_assignments(variables):
        if is_satisfiable(clauses, assignment):
            return assignment
    return None

# Reduction from SAT to 3SAT
def reduce_sat_to_3sat(clauses):
    """
    Converts a general CNF formula to an equivalent 3SAT formula.
    Each clause is transformed to 3 literals using standard techniques.
    """
    def pad_clause(clause):
        # Clause has < 3 literals: pad it with duplicates
        while len(clause) < 3:
            clause.append(clause[-1])
        return clause

    new_clauses = []
    counter = 1

    for clause in clauses:
        if len(clause) == 3:
            new_clauses.append(clause)
        elif len(clause) < 3:
            new_clauses.append(pad_clause(clause.copy()))
        else:
            # Break clause with >3 literals into 3-literal clauses
            new_vars = []
            for i in range(len(clause) - 3):
                y = f"y{counter}"
                counter += 1
                new_vars.append(y)

            # First clause
            new_clauses.append([clause[0], clause[1], new_vars[0]])

            # Middle clauses
            for i in range(1, len(new_vars)):
                new_clauses.append([f"-{new_vars[i - 1]}", clause[i + 1], new_vars[i]])

            # Last clause
            new_clauses.append([f"-{new_vars[-1]}", clause[-2], clause[-1]])

    return new_clauses

# Example Usage
if __name__ == "__main__":
    print("=== SAT Solver ===")
    sat_formula = [['x1', '-x2'], ['x2', 'x3'], ['-x1', '-x3']]
    result = solve_sat(sat_formula)
    if result:
        print("SATISFIABLE: Assignment =", result)
    else:
        print("UNSATISFIABLE")

    print("\n=== SAT to 3SAT Reduction ===")
    general_formula = [['x1', 'x2', 'x3', 'x4'], ['x2'], ['-x1', '-x3']]
    converted = reduce_sat_to_3sat(general_formula)
    print("Original:", general_formula)
    print("Converted to 3SAT:", converted)

    # Verify if the same assignment works (if possible)
    if result:
        print("\nChecking converted 3SAT with same assignment...")
        print("Satisfiable?", is_satisfiable(converted, result))
