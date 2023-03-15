# Minimum Cardinality Subset of Bases to Arm

## Overview

The purpose of this project is to solve the Minimum Cardinality Subset of Bases to Arm problem. Given an undirected graph representing military bases and their mutual protections, and some critical points that need to be protected, the objective is to find the minimum subset of bases that need to be armed to protect all critical points.

## Problem Description

The Minimum Cardinality Subset of Bases to Arm problem is a variant of the Minimum Dominating Set problem, where we aim to minimize the cardinality of the set of vertices in a graph such that all critical points are either in the set or are adjacent to a vertex in the set.

## How to Run the Code

1. Clone this repository: `git clone https://github.com/your_username/minimum-cardinality-subset-of-bases-to-arm.git`.
2. Navigate to the project directory: `cd minimum-cardinality-subset-of-bases-to-arm`.
3. Install the required dependencies: `pip install -r requirements.txt`.
4. Run the `base_defense.py` file: `python base_defense.py`.
5. The program will generate a random graph of military bases, visualize it, and solve the Minimum Cardinality Subset of Bases to Arm problem using AMPL. The resulting minimum subset of bases to arm will be visualized and printed to the console.

## Dependencies

- Python 3.6+
- See requirements.txt for the required packages
- AMPL

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/<username>/<repository>.git
    cd <repository>
    ```

2. Install the required packages using pip:

    ```sh
    pip install -r requirements.txt
    ```

    For running experiments that use different versions of the greedy algorithm, install the packages from requirements_greedy.txt:

    ```sh
    pip install -r requirements_greedy.txt
    ```

## Usage

The program generates a random graph of military bases and identifies the critical bases that need to be protected. It then uses integer linear programming to find the minimum subset of bases that need to be armed to protect all critical points.

The output of the program is a visual representation of the graph, with the critical bases marked in red and the minimum subset of bases to arm marked with a diamond shape.

1. To run the main script that generates a graph of bases, saves it to PDF and DAT formats, and runs the AMPL model on the DAT file, run:

    ```sh
    python main.py
    ```

2. To run experiments on different versions of the greedy algorithm, run:

    ```sh
    python experiments_greedy.py
    ```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions to the project are welcome. If you find any bugs or issues, please create an issue in the project repository. Pull requests for bug fixes, new features, or improvements are also welcome.
