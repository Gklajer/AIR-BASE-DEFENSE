import math
import time
import networkx as nx
import functools

# HELPER FUNCTIONS
def timer(func: "function") -> "function":
    """
    Timer decorator

    Parameters
    ----------
    func
        function to decorate
    """

    # Define a closure that takes a list as an argument and returns the wrapper function
    @functools.wraps(func)
    def make_wrapper(time_list):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            # Append the time result to the list
            time_list.append(end - start)

            print(
                f"Function {func.__name__} took {end-start:.4f}s to execute."
            )

            return result

        return wrapper

    # Return the closure with an empty list as the default argument
    return make_wrapper([])


def _euclidean_distance(u_pos: tuple, v_pos: tuple):
    """
    Compute euclidean distance

    Parameters
    ----------
    u_pos, v_pos
        points position in the plane

    Returns
    -------
        euclidean distance
    """
    return math.sqrt((u_pos[0] - v_pos[0]) ** 2 + (u_pos[1] - v_pos[1]) ** 2)


def _remove_long_edges(
    graph: nx.Graph,
    pos: dict[int, (float, float)],
    radius: float,
) -> None:
    """
    Remove edges between distant points

    Parameters
    ----------
    graph
        the bases graph
    pos
        position of the graph in the plane
    radius
        threshold for the bases to be connected
    """
    for u, v in list(graph.edges()):
        if _euclidean_distance(pos[u], pos[v]) > radius:
            graph.remove_edge(u, v)
