"""Random Graph of Bases to Defend Generation + Visualization + Solution"""

# IMPORTS
import math
import os
import subprocess
import networkx as nx
from utils import *
from utils.helpers import timer


def dot_to_pdf(
    source_filename: str,
    dest_filename: str,
    pos: dict[int, (float, float)],
    colormap: dict[str, str] = constants.COLORMAP,
    shapemap: dict[str, str] = constants.SHAPEMAP,
) -> None:
    """
    Save the graph described in the .dot file inside a .pdf file

    Parameters
    ----------
    source_filename
        name of the source file
    dest_filename
        name of the destination file
    pos
        position of the graph in the plane
    colormap, optional
        color map (attr -> color) for the plot, by default `COLORMAP`
    shapemap, optional
        shape map (attr -> shape) for the plot, by default `SHAPEMAP`
    """
    graph: nx.Graph = nx.drawing.nx_pydot.read_dot(f"{source_filename}.dot")
    core.graph_to_pdf(graph, pos, dest_filename, colormap, shapemap)


def graph_to_dat(
    graph: nx.Graph,
    dest_filename: str,
    is_critical_point_to_lab: dict[
        bool, str
    ] = constants.IS_CRITICAL_POINT_TO_LAB,
    colormap: dict[str, str] = constants.COLORMAP,
) -> None:
    """
    Write graph's description inside a .dot file

    Parameters
    ----------
    graph
        graph to export
    dest_filename
        name of the file to write in
    is_critical_point_to_lab, optional
        map (True/False -> label), by default `IS_CRITICAL_POINT_TO_LAB`
    colormap, optional
        color map (attr -> color) for the plot, by default `COLORMAP`
    """
    with open(f"{dest_filename}.dat", "w") as f:
        # Write the bases
        f.write("# bases\n")
        f.write("param : V : is_critical_point :=\n")
        for base_label, base in graph.nodes.items():
            critical_point_color = colormap[is_critical_point_to_lab[True]]
            base_to_defend = base["fillcolor"] == critical_point_color

            f.write(f"  {base_label} {int(base_to_defend)}\n")
        f.write(";\n\n")

        # Write the connections
        f.write("# connections\n")
        f.write("set E :=\n")
        for edge in graph.edges(data=True):
            f.write(f"  {edge[0]} {edge[1]}\n")
        f.write(";")


@timer
def run_ampl_timed(filename: str = constants.FILENAME):
    subprocess.run(["ampl", f"{filename}.run"])


def run_ampl(
    dirname: str = constants.DIR_AMPL, filename: str = constants.FILENAME
):
    """
    run ampl file

    Parameters
    ----------
    dirname
        name of the directory containing ampl files
    filename
        name of the ampl files
    """
    os.chdir(dirname)

    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/ampl")

    run_ampl_timed()

    os.chdir("..")


# "Main" script
if __name__ == "__main__":
    bases_graph, pos, _ = core.generate_graph_of_bases(
        **constants.GENERATE_GRAPH_OF_BASES_DEFAULT_KWARGS
    )

    core.graph_to_pdf(bases_graph, pos, constants.FILENAME)

    graph_to_dat(
        bases_graph, os.path.join(constants.DIR_AMPL, constants.FILENAME)
    )

    run_ampl(dirname=constants.DIR_AMPL, filename=constants.FILENAME)

    dot_to_pdf(
        source_filename=os.path.join(
            constants.DIR_AMPL, constants.RESULT_FILENAME
        ),
        dest_filename=constants.RESULT_FILENAME,
        pos=pos,
    )
