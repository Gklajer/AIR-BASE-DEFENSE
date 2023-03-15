# "Core" functions
import math
import random
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from utils.constants import (
    COLORMAP,
    EDGE_COLOR,
    SEED,
    IS_CRITICAL_POINT_TO_LAB,
    SHAPEMAP,
)
import numpy.random as npr
import networkx as nx

from utils.helpers import _remove_long_edges, timer


@timer
def generate_graph_of_bases(
    number_bases: int,
    proba: float,
    radius: float,
    seed: int,
    is_critical_point_to_lab: dict[bool, str] = IS_CRITICAL_POINT_TO_LAB,
    colormap: dict[str, str] = COLORMAP,
) -> tuple:
    """
    Generate a graph (undirected) with some critical points (bases to defend) for nodes and connections (one base can protect the other base) for edges

    Parameters
    ----------
    number_bases
        number of nodes
    proba
        probability of the binomial law to draw edges
    radius
        Distance threshold value to place a random edges
    is_critical_point_to_lab, optional
        map (True/False -> label), by default `IS_CRITICAL_POINT_TO_LAB`
    colormap, optional
        color map (attr -> color) for the plot, by default `COLORMAP`

    Returns
    -------
        the (undirected) graph of bases, its position in the plane and the list of critical points
    """

    npr.seed(seed)
    
    graph: nx.Graph = nx.fast_gnp_random_graph(
        number_bases, proba, seed, directed=False
    )
    pos: dict[int, (float, float)] = nx.spring_layout(graph)

    _remove_long_edges(graph, pos, radius)

    number_bases_to_def = npr.randint(0, number_bases)

    random.seed(seed)
    bases_to_def = random.sample(range(number_bases), number_bases_to_def)

    for base_idx, base in graph.nodes.items():
        is_base_to_def = base_idx in bases_to_def
        base["fillcolor"] = colormap[is_critical_point_to_lab[is_base_to_def]]
        base["shape"] = "o"

    new_labels = {
        base_idx: f"base{base_idx}" for base_idx in graph.nodes.keys()
    }

    critical_points = [new_labels[base_to_def] for base_to_def in bases_to_def]
    relabeled_graph = nx.relabel_nodes(graph, new_labels)
    relabeled_pos = {
        new_labels[old_label]: pos_base for old_label, pos_base in pos.items()
    }

    return relabeled_graph, relabeled_pos, critical_points


def graph_to_pdf(
    graph: nx.Graph,
    pos: dict[int, (float, float)],
    dest_filename: str,
    colormap: dict[str, str] = COLORMAP,
    shapemap: dict[str, str] = {"base": "o"},
    edge_color: str = EDGE_COLOR,
) -> None:
    """
    Save the graph as in a pdf file

    Parameters
    ----------
    graph
        graph to save
    pos
        position of the graph in the plane
    dest_filename
        name of the destination file
    colormap, optional
        color map (attr -> color) for the plot, by default `COLORMAP`
    shapemap, optional
        shape map (attr -> shape) for the plot, by default `{"base": "o"}`
    """
    data = graph.nodes(data=True)

    fig = plt.figure(num=1, clear=True)
    for shape_symb in shapemap.values():
        nodelist = [node for node, attr in data if attr["shape"] == shape_symb]
        colors = [
            graph.nodes[node].get("fillcolor", "none") for node in nodelist
        ]
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=nodelist,
            node_color=colors,
            node_shape=shape_symb,
            edgecolors=edge_color,
            node_size=(
                node_size := 6000 / (num_nodes := graph.number_of_nodes())
            ),
            linewidths=10 / math.sqrt(num_nodes),
        )

    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color=edge_color,
        node_size=node_size,
        width=5 / math.sqrt(num_nodes),
    )

    nx.draw_networkx_labels(graph, pos, font_size=80 / num_nodes)

    legend_elements = []

    if colormap != None:
        legend_elements += [
            Patch(facecolor=color_symb, edgecolor=edge_color, label=color_lab)
            for color_lab, color_symb in colormap.items()
        ]
        Patch(facecolor="w", edgecolor=edge_color, label="normal"),

    if shapemap != None:
        legend_elements += [
            Line2D(
                [],
                [],
                lw=0,
                color="w",
                mfc="w",
                markeredgecolor=edge_color,
                marker=shape_symb,
                label=shape_lab,
                markersize=12,
            )
            for shape_lab, shape_symb in shapemap.items()
        ]

    # Add legend for base type
    fig.legend(handles=legend_elements, title="Base type")

    fig.savefig(f"{dest_filename}.pdf", format="pdf")


def set_attributes(
    bases_graph: nx.Graph,
    bases_to_arm: list[str],
    critical_points: list[str],
    is_critical_point_to_lab: dict[bool, str] = IS_CRITICAL_POINT_TO_LAB,
    colormap: dict[str, str] = COLORMAP,
    shapemap: dict[str, str] = SHAPEMAP,
):
    """
     Set attributes color and shape for the nodes of the bases graph.

    Parameters
    ----------
    bases_graph : networkx.Graph
        The graph of the bases.
    bases_to_arm : list[str]
        The list of bases to arm.
    critical_points : list[str]
        The list of critical points.
    is_critical_point_to_lab, optional
        dict (True/False -> lab), by default IS_CRITICAL_POINT_TO_LAB
    colormap, optional
        dict (lab -> color), by default COLORMAP
    shapemap, optional
        dict (lab -> shape), by default SHAPEMAP
    """

    # Loop through all the nodes in the graph
    for node in bases_graph.nodes():
        # Assign the attributes to the node
        bases_graph.nodes[node]["fillcolor"] = colormap[
            is_critical_point_to_lab[node in critical_points]
        ]

        bases_graph.nodes[node]["shape"] = shapemap[
            "to arm" if node in bases_to_arm else "to leave unarmed"
        ]

