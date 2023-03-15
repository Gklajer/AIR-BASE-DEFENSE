import math

# CONSTANT PARAMETERS
SEED = 8
NUMBER_BASES = 20
NUMBER_GRAPHS = 1
PROBABILITY_EDGE_CREATION = 0.5
RADIUS_THRESHOLD_EDGE = 2 / math.sqrt(NUMBER_BASES)

GENERATE_GRAPH_OF_BASES_DEFAULT_KWARGS = {
    "number_bases": NUMBER_BASES,
    "proba": PROBABILITY_EDGE_CREATION,
    "radius": RADIUS_THRESHOLD_EDGE,
    "seed": SEED,
}

IS_CRITICAL_POINT_TO_LAB = {True: "to defend", False: "normal"}
COLORMAP = {
    IS_CRITICAL_POINT_TO_LAB[True]: "red",
    IS_CRITICAL_POINT_TO_LAB[False]: "none",
}

SHAPEMAP = {"to arm": "D", "to leave unarmed": "o"}

EDGE_COLOR = "black"

DIR_AMPL = "AMPL"
FILENAME = "base_defense"
RESULT_FILENAME = f"result_{FILENAME}"
