def greedy_hitting_set(S):
    """
    Solves the Hitting Set problem using a greedy algorithm.

    Args:
        S: A list of sets representing the hypergraph (set system)

    Returns:
        A hitting set (a set that intersects every set in S)
    """
    remaining_sets = [set(ss) for ss in S]
    hitting_set = set()

    while remaining_sets:
        element_counts = {}
        for s in remaining_sets:
            for element in s:
                element_counts[element] = element_counts.get(element, 0) + 1

        if not element_counts:
            break

        best_element = max(element_counts.keys(), key=lambda x: element_counts[x])
        hitting_set.add(best_element)

        remaining_sets = [s for s in remaining_sets if best_element not in s]

    return hitting_set


if __name__ == "__main__":
    S = [
        {1, 2, 3},
        {2, 4},
        {3, 5},
        {4, 5, 6},
        {1, 5}
    ]

    hs = greedy_hitting_set(S)
    print("Hitting Set:", hs)

    for subset in S:
        assert hs & subset, f"Error: Hitting set {hs} doesn't intersect with {subset}"
    print("Verification passed - it's a valid hitting set")