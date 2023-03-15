from experiments_greedy import greedy_dominating_set_v2 as find_dominating_set
import metis
import networkx as nx
from concurrent.futures import ThreadPoolExecutor


def find_dominating_set_parallel(graphs: list[nx.Graph], critical_points):
    # Create a thread pool
    with ThreadPoolExecutor() as executor:
        # Submit tasks to find dominating set for each subgraph
        futures = [
            executor.submit(find_dominating_set, graph, critical_points)
            for graph in graphs
        ]

        # Wait for all tasks to complete and collect results
        results = [future.result() for future in futures]

    # Combine results from all subgraphs
    dominating_set = set().union(*results)

    return list(dominating_set)


def partition_graph(graph: nx.Graph, k: int):

    # Set metis options
    options = metis.MetisOptions(
        objtype=metis.MetisObjType.cut,
        ctype=metis.MetisCType.shem,
        iptype=metis.MetisIPType.grow,
        rtype=metis.MetisRType.fm,
        ncuts=1,
        niter=10,
        ufactor=30,
    )

    # Compute the partition using metis
    _, parts = metis.part_graph(graph, k, options=options)

    # Create subgraphs from the partition
    subgraphs = []
    for i in range(k):
        nodes = [node for node, part in zip(graph.nodes(), parts) if part == i]
        subgraph = graph.subgraph(nodes)
        subgraphs.append(subgraph)

    return subgraphs


def reduce_dominating_set(graph: nx.Graph, dominating_set):
    # Create a copy of the dominating set
    reduced_dominating_set = list(dominating_set)

    # Iterate over vertices in the dominating set
    for vertex in dominating_set:
        # Check if removing the vertex from the dominating set would still result in a valid dominating set
        if all(
            neighbor in reduced_dominating_set
            for neighbor in graph.neighbors(vertex)
        ):
            reduced_dominating_set.remove(vertex)

    return reduced_dominating_set
