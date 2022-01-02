import multiprocessing
import os
import numpy as np
import time
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

    def _particle_init(self, p_id, mat_size, label_size, global_pos_dict, global_vel_dict, global_fit_dict):
        np.random.seed((os.getpid() * int(time.time())) % 123456789)

        p_vel = np.random.dirichlet(np.ones(label_size), size=mat_size)
        p_best_pos = np.random.randint(label_size, size=mat_size)
        p_best_fit = self._fitness_func(p_best_pos)

        global_pos_dict[p_id] = p_best_pos
        global_vel_dict[p_id] = p_vel
        global_fit_dict[p_id] = p_best_fit

    def nature(self, num_of_particles: int = 0, max_iter: int = 10000):
        """
        Solves the provided problem instance using the implemented nature-inspired PSO algorithm.
        """
        print("Solving with the nature inspired algorithm...")

        # Step 1 - Initialization
        particles = []
        manager = multiprocessing.Manager()
        global_pos_dict, global_vel_dict, global_fit_dict = manager.dict(), manager.dict(), manager.dict()
        for i in range(num_of_particles):
            p = multiprocessing.Process(target=self._particle_init,
                                        args=(i, self.incidence_matrix.shape[0], 4,
                                              global_pos_dict, global_vel_dict, global_fit_dict))
            particles.append(p)
            p.start()

        for p in particles:
            p.join()

        # Step 2 - Loop end check - fitness 0 or max iterations reached
        global_pos = global_pos_dict[min(global_fit_dict, key=global_fit_dict.get)]
        global_fit = global_fit_dict[min(global_fit_dict, key=global_fit_dict.get)]
        iter_counter = 1
        while global_fit != 0 and iter_counter <= max_iter:
            iter_counter += 1
            # Step 3 - Main loop of particle movement