import sys
import numpy as np

import utils
from utils import read_instance
from itertools import product


class Solve:
    """
    Utility for solving the provided problem instance and saving the results in the solved-instance directory.
    The instance must exist within problem-instances directory
    :param filename: the name of the problem instance
    :param index_row: a flag indicating whether the first row contains headers (default: True)
    :param index_col: a flag indicating whether the first column contains headers (default: False)
    """
    def __init__(self, filename: str, index_row: bool = True, index_col: bool = False):
        self.filename = filename
        self.incidence_matrix = read_instance(filename, index_row, index_col, output='numpy')

    def _fitness_func(self, solution: np.array = None):
        fitness = 0
        for i, node_incidence in enumerate(self.incidence_matrix):
            inode_label = solution[i]
            node_neighbors = solution[np.array(node_incidence, dtype=bool)]
            conflicts = inode_label == node_neighbors
            fitness += np.count_nonzero(conflicts)

        return fitness

    def reference(self):
        """
        Solves the provided problem instance using the implemented reference algorithm - brute force.
        """
        print("Solving with the reference algorithm...")

        mat_size = self.incidence_matrix.shape[0]
        best_fit_sol = np.zeros(mat_size)
        best_fit_val = self._fitness_func(best_fit_sol)
        solution_set = product([0, 1, 2, 3], repeat=mat_size)

        for i in list(solution_set):
            cand_solution = np.array(i)
            cand_fitness = self._fitness_func(cand_solution)
            if cand_fitness < best_fit_val:
                best_fit_val = cand_fitness
                best_fit_sol = cand_solution

        print('Saving the best solution found: ' + str(best_fit_sol) + '\nwith the fitness value: ' + str(best_fit_val))
        utils.save_solution(self.filename, best_fit_sol)

    def nature(self):
        """
        Solves the provided problem instance using the implemented nature-inspired PSO algorithm.
        """
        print("Solving with the nature inspired algorithm...")
        # self._fitness_func(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))