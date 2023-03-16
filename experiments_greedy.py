"""Following greedy algorithms for finding a dominating set for a given graph and a set of critical points. It iteratively selects the vertex that covers the maximum number of uncovered critical points and adds it to the dominating set until all critical points are covered.

There are other algorithms for finding dominating sets in graphs. Some of these algorithms use exact methods such as integer programming or branch-and-bound to find an optimal solution, while others use heuristic or approximation algorithms to find near-optimal solutions.

Exact algorithms can guarantee an optimal solution but may have exponential time complexity and may not be practical for large graphs. Heuristic and approximation algorithms can provide near-optimal solutions in polynomial time but do not guarantee optimality.

It provides a simple and efficient way to find a near-optimal solution in polynomial time. 

However, it does not guarantee an optimal solution and its performance may vary depending on the input graph and the set of critical points."""


import heapq
import networkx as nx
from utils import *
from utils.helpers import timer


@timer
def greedy_dominating_set_v0(graph: nx.Graph, critical_points):
    """
    Find a greedy approximate of the minimum dominating set for the given graph with its critical points
    
    Parameters
    ----------
    graph 
        An undirected graph represented as a networkx Graph object.
    critical_points
        A list of critical points that must be covered by the dominating set.
    
    Return
    ------
    A list of vertices representing an approximate minimum dominating set for the given graph and critical points.
    
    Analysis
    --------
    Multiplicative approximation error factor: ln(D) + 1 (where D: maximum degree of a vertex over the entire graph)

    Worst-case time complexity: O(n^2) (where n := card(V))\\
    In each iteration of the while loop check all vertices in the graph to find the one that covers the maximum number of uncovered critical points
    
    Worst-case space complexity: O(n)\\
    Store uncovered critical points and dominating set
    """
    # Initialize the dominating set and uncovered critical points
    dominating_set = []
    uncovered = set(critical_points)

    # Iterate until all critical points are covered
    while uncovered:
        # Find the vertex that covers the maximum number of uncovered critical points
        max_cover = 0
        max_vertex = None
        for vertex in graph.nodes():
            can_protect = set(graph.adj[vertex]) | {vertex}
            cover = len(uncovered & can_protect)
            # print(cover)
            if cover > max_cover:
                max_cover = cover
                max_vertex = vertex

        # Add the vertex to the dominating set and update the uncovered critical points
        dominating_set.append(max_vertex)
        uncovered -= (covered := set(graph.adj[max_vertex]) | {max_vertex})
    return dominating_set


"""Additional optimizations"""

# 1. reduced average-case time complexity
@timer
def greedy_dominating_set_v1(graph: nx.Graph, critical_points):
    # Initialize the dominating set and uncovered critical points
    dominating_set = []
    uncovered = set(critical_points)
    remaining_vertices = set(graph.nodes())

    # Iterate until all critical points are covered
    while uncovered:
        # Find the vertex that covers the maximum number of uncovered critical points
        max_cover = 0
        max_vertex = None
        for vertex in remaining_vertices:
            can_protect = set(graph.adj[vertex]) | {vertex}
            cover = len(uncovered & can_protect)
            if cover > max_cover:
                max_cover = cover
                max_vertex = vertex

        # Add the vertex to the dominating set and update remaining vertices and uncovered critical points
        dominating_set.append(max_vertex)
        remaining_vertices.remove(max_vertex)
        uncovered -= (covered := set(graph.adj[max_vertex]) | {max_vertex})
    return dominating_set


@timer
def greedy_dominating_set_v2(graph, critical_points):
    """2. Preprocessing optimizations

    Before starting the while loop:

    -remove not critical points without any critical neighbours (because: will never be selected as max_vertex) \n
    -treat isolated (no neighbour) critical points separatly
    """

    # Initialize the dominating set and uncovered critical points
    dominating_set = []
    uncovered = set(critical_points)

    # Preprocess the graph to remove any vertices that are not critical points and have no neighbors that are critical points
    remaining_vertices = set()
    for vertex in graph.nodes():
        if vertex in uncovered:
            if not any(True for _ in graph.neighbors(vertex)):
                # Add isolated critical point directly to dominating set
                dominating_set.append(vertex)
                uncovered.remove(vertex)
            else:
                remaining_vertices.add(vertex)
        elif any(
            neighbor in uncovered for neighbor in graph.neighbors(vertex)
        ):
            remaining_vertices.add(vertex)

    # Iterate until all critical points are covered
    while uncovered:
        # Find the vertex that covers the maximum number of uncovered critical points
        max_cover = 0
        max_vertex = None
        for vertex in remaining_vertices:

            can_protect = set(graph.adj[vertex]) | {vertex}
            cover = len(uncovered & can_protect)
            if cover > max_cover:
                max_cover = cover
                max_vertex = vertex

        # Add the vertex to the dominating set and remove its neighbors from consideration
        dominating_set.append(max_vertex)
        remaining_vertices.remove(max_vertex)

        uncovered -= (covered := set(graph.adj[max_vertex]) | {max_vertex})
    return dominating_set


@timer
def greedy_dominating_set_v3_0(graph, critical_points):
    """3.0 (Binary heap as) Priority Queue - reduce the time to find max cover vertex (O(n) -> O(log n) time) \n

    Keep track of the vertices in remaining_vertices sorted by their cover value
    """
    # Initialize the dominating set and uncovered critical points
    dominating_set = []
    uncovered = set(critical_points)

    remaining_vertices = set()
    for vertex in graph.nodes():
        if vertex in uncovered:
            if not any(True for _ in graph.neighbors(vertex)):
                # Add isolated critical point directly to dominating set
                dominating_set.append(vertex)
                uncovered.remove(vertex)
            else:
                remaining_vertices.add(vertex)
        elif any(
            neighbor in uncovered for neighbor in graph.neighbors(vertex)
        ):
            remaining_vertices.add(vertex)

    # Initialize priority queue with vertices sorted by cover value
    pq = []
    for vertex in remaining_vertices:
        can_protect = set(graph.adj[vertex]) | {vertex}
        cover = len(uncovered & can_protect)
        heapq.heappush(pq, (-cover, vertex))

    # Iterate until all critical points are covered
    while uncovered:
        # Find the vertex that covers the maximum number of uncovered critical points
        max_cover, max_vertex = heapq.heappop(pq)
        max_cover = -max_cover

        # Add max_vertex to the dominating set and update uncovered
        dominating_set.append(max_vertex)
        uncovered -= (covered := set(graph.adj[max_vertex]) | {max_vertex})

        # Update priority queue with new cover values
        pq = [
            (-len(uncovered & (can_protect := set(graph.adj[v]) | {v})), v)
            for _, v in pq
        ]
        heapq.heapify(pq)

    return dominating_set


# Problem: maintain heap structure O(n log n) (overall : O(n^2 log n))

if __name__ == "__main__":
    bases_graph, pos, critical_points = core.generate_graph_of_bases(
        **constants.GENERATE_GRAPH_OF_BASES_DEFAULT_KWARGS
    )

    bases_to_arm = greedy_dominating_set_v2(bases_graph, critical_points)
    core.set_attributes(bases_graph, bases_to_arm, critical_points)

    core.graph_to_pdf(
        bases_graph,
        pos,
        "greedy_" + constants.FILENAME,
        shapemap=constants.SHAPEMAP,
    )
