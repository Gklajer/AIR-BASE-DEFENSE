import os
from base_defense import graph_to_dat, run_ampl
from experiments_greedy import greedy_dominating_set_v2 as find_dominating_set
import metis
import networkx as nx
from concurrent.futures import ThreadPoolExecutor

from utils import *


def find_dominating_set_parallel(graph: nx.Graph, critical_points: list[str], find_dominating_set: "function", k: int):
    graphs = partition_graph(graph, k)
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

    return reduce_dominating_set(list(dominating_set))


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


def reduce_dominating_set(graph: nx.Graph, dominating_set: list["str"]):
    # Create a copy of the dominating set
    reduced_dominating_set = dominating_set.copy()

    # Iterate over vertices in the dominating set
    for vertex in dominating_set:
        # Check if removing the vertex from the dominating set would still result in a valid dominating set
        if all(
            neighbor in reduced_dominating_set
            for neighbor in graph.neighbors(vertex)
        ):
            reduced_dominating_set.remove(vertex)

    return reduced_dominating_set

if __name__ == "__main__":
    bases_graph, pos, critical_points = core.generate_graph_of_bases(
            **constants.GENERATE_GRAPH_OF_BASES_DEFAULT_KWARGS
        )

    bases_to_arm = find_dominating_set_parallel(bases_graph, critical_points, find_dominating_set, k=3)
    
    core.set_attributes(bases_graph, bases_to_arm, critical_points)

    core.graph_to_pdf(
        bases_graph,
        pos,
        "parallel" + constants.FILENAME,
        shapemap=constants.SHAPEMAP,
    )
