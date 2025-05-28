# Unit-IV Sets and Partitions: Set partition, Set Cover, Subset Sum and Knapsack Problem.

import itertools

# 1. SET PARTITION PROBLEM
def can_partition_set(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    n = len(nums)
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] |= dp[i - num]
    return dp[target]

# 2. SET COVER PROBLEM
def set_cover(universe, subsets):
    best_cover = None
    for r in range(1, len(subsets)+1):
        for combo in itertools.combinations(subsets, r):
            union = set().union(*combo)
            if union == universe:
                best_cover = combo
                return best_cover
    return None

# 3. SUBSET SUM PROBLEM
def has_subset_sum(nums, target):
    n = len(nums)
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] |= dp[i - num]
    return dp[target]

# 4. KNAPSACK PROBLEM (0/1 Knapsack)
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]

# === Sample Usage ===
if __name__ == "__main__":
    # Set Partition
    print("=== Set Partition ===")
    nums = [1, 5, 11, 5]
    print("Can partition:", can_partition_set(nums))

    # Set Cover
    print("\n=== Set Cover ===")
    universe = {1, 2, 3, 4, 5}
    subsets = [{1, 2}, {2, 3}, {4}, {3, 4, 5}]
    cover = set_cover(universe, subsets)
    print("Set cover found:" if cover else "No cover found")
    if cover:
        print("Cover:", cover)

    # Subset Sum
    print("\n=== Subset Sum ===")
    nums = [3, 34, 4, 12, 5, 2]
    target = 9
    print("Subset with sum", target, "exists:", has_subset_sum(nums, target))

    # Knapsack
    print("\n=== Knapsack ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    print("Maximum value in knapsack:", knapsack(values, weights, capacity))
