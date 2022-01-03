import multiprocessing
import os
import sys
import numpy as np
import time
from utils import read_instance, save_solution
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
        save_solution(self.filename, best_fit_sol)

    def _particle_init(self, p_id, mat_size, label_size,
                       pos_curr_dict, pos_prev_dict, vel_dict, pbest_dict):

        np.random.seed((os.getpid() * int(time.time())) % 123456789)

        p_init_vel = 1.0
        p_init_pos = np.random.randint(label_size, size=mat_size)

        pos_prev_dict[p_id] = np.full(self.incidence_matrix.shape[0], -1)
        pos_curr_dict[p_id] = p_init_pos
        vel_dict[p_id] = p_init_vel
        pbest_dict[p_id] = p_init_pos

    def _particle_movement(self, p_id, w, c1, c2, global_best_pos,
                           pos_curr_dict, pos_prev_dict, vel_dict, pbest_dict):

        np.random.seed((os.getpid() * int(time.time())) % 123456789)
        pos_curr = pos_curr_dict[p_id]
        p_best_pos = pbest_dict[p_id]
        n = float(len(pos_curr))

        if (pos_prev_dict[p_id] == np.full(self.incidence_matrix.shape[0], -1)).all():
            p_vel = w * vel_dict[p_id]
        else:
            p_vel = 1 - (np.count_nonzero(pos_curr != pos_prev_dict[p_id]) / n)

        vel_dict[p_id] = p_vel
        pos_prev_dict[p_id] = pos_curr

        v_rand = w * p_vel
        vp_best = c1 * np.random.uniform(0, 1) * (
                1 - (np.count_nonzero(pos_curr != p_best_pos) / n))
        vg_best = c2 * np.random.uniform(0, 1) * (
                1 - (np.count_nonzero(pos_curr != global_best_pos) / n))
        v = v_rand + vg_best + vp_best
        p_rand = v_rand / v
        pp_best = vp_best / v
        pg_best = vg_best / v

        for i, _ in enumerate(pos_curr):
            r = np.random.uniform(0, 1)
            if r <= p_rand:
                pos_curr[i] = np.random.choice([0, 1, 2, 3])
            elif r <= p_rand + pp_best:
                pos_curr[i] = p_best_pos[i]
            else:
                pos_curr[i] = global_best_pos[i]
        pos_curr_dict[p_id] = pos_curr

        fitness_curr = self._fitness_func(pos_curr)
        fitness_best = self._fitness_func(pbest_dict[p_id])
        if fitness_curr < fitness_best:
            pbest_dict[p_id] = pos_curr

    def nature(self, num_of_particles: int = 0, max_iter: int = 10000,
               w: float = 0.8, c1: float = 0.1, c2: float = 0.1):
        """
        Solves the provided problem instance using the implemented nature-inspired PSO algorithm.
        """
        print("Solving with the nature inspired algorithm...")

        # Step 1 - Initialization
        particles = []
        manager = multiprocessing.Manager()
        # common_dict = manager.dict()
        pos_curr_dict, pos_prev_dict, vel_dict, pbest_dict = manager.dict(), manager.dict(), manager.dict(), manager.dict()
        # common_dict['pos_curr'], common_dict['pos_prev'], common_dict['vel'], common_dict['pbest'] = {}, {}, {}, {}
        for i in range(num_of_particles):
            p = multiprocessing.Process(target=self._particle_init,
                                        args=(i, self.incidence_matrix.shape[0], 4,
                                              pos_curr_dict, pos_prev_dict, vel_dict, pbest_dict))
            particles.append(p)
            p.start()

        for p in particles:
            p.join()

        global_best_fit = sys.maxsize
        global_best_pos = np.zeros(self.incidence_matrix.shape[0])
        for pos in pbest_dict.values():
            pbest_fitness = self._fitness_func(pos)
            if pbest_fitness < global_best_fit:
                global_best_fit = pbest_fitness
                global_best_pos = pos

        print(pos_prev_dict, pos_curr_dict, vel_dict, pbest_dict)
        # Step 2 - Loop end check - fitness 0 or max iterations reached
        iter_counter = 1
        while global_best_fit != 0 and iter_counter <= max_iter:
            # Step 3 - Main loop of the particle movement
            particles = []
            for i in range(num_of_particles):
                p = multiprocessing.Process(target=self._particle_movement,
                                            args=(i, w, c1, c2, global_best_pos,
                                                  pos_curr_dict, pos_prev_dict, vel_dict, pbest_dict))
                particles.append(p)
                p.start()

            for p in particles:
                p.join()

            for pos in pbest_dict.values():
                pbest_fitness = self._fitness_func(pos)
                if pbest_fitness < global_best_fit:
                    global_best_fit = pbest_fitness
                    global_best_pos = pos

            iter_counter += 1

        print('Saving the best solution found: ' + str(global_best_pos)
              + '\nwith the fitness value: ' + str(global_best_fit))
        save_solution(self.filename, global_best_pos)
