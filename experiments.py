import os
import json
import numpy as np
import pandas as pd
from algorithms import Solve


class Experiment:
    """
    Utility for conducting automated experiment-instances on the implemented algorithms
    :param filename: the name of the experiment instance in the experiment-instances directory (.json files)
    """

    def __init__(self, filename: str):
        self.filename = filename

    def param_steering(self):
        experiment_path = os.path.join(os.path.dirname(__file__), 'experiment-instances', self.filename)
        with open(experiment_path, 'r') as f:
            exp_data = json.load(f)

        if exp_data['algorithm'] == 'nature':
            param_list = ['w', 'c1', 'c2', 'num_of_particles', 'max_iter']
            steered_param = exp_data['steered_param']['name']

            if steered_param not in param_list:
                print('Wrong paramater for steering specified!')
                return

            results_list = []
            tested_val = np.float32(exp_data['steered_param']['min_val'])
            max_val = np.float32(exp_data['steered_param']['max_val'])
            step = np.float32(exp_data['steered_param']['step'])
            repetitions = exp_data['steered_param']['repetitions']
            while tested_val <= max_val:
                print('Number ' + str(exp_data['steered_param']['repetitions'] - repetitions + 1)
                      + ' repetition of parameter with value ' + str(tested_val) + ' running...')

                w = tested_val \
                    if exp_data['steered_param']['name'] == 'w' \
                    else exp_data['other_params']['w']
                c1 = tested_val \
                    if exp_data['steered_param']['name'] == 'c1' \
                    else exp_data['other_params']['c1']
                c2 = tested_val \
                    if exp_data['steered_param']['name'] == 'c2' \
                    else exp_data['other_params']['c2']
                num_of_particles = tested_val \
                    if exp_data['steered_param']['name'] == 'num_of_particles' \
                    else exp_data['other_params']['num_of_particles']
                max_iter = tested_val \
                    if exp_data['steered_param']['name'] == 'max_iter' \
                    else exp_data['other_params']['max_iter']

                experiment = Solve(exp_data['other_params']['filename'])
                fitness, time = experiment.nature(num_of_particles, max_iter, w, c1, c2, supress_logs=True)

                results_row = [tested_val, fitness, time]
                results_list.append(results_row)

                repetitions -= 1
                if repetitions == 0:
                    tested_val += step
                    repetitions = exp_data['steered_param']['repetitions']

            df = pd.DataFrame(results_list, columns=['Steered Parameter Value', 'Fitness', 'Time'])
            df.to_csv(os.path.join(os.path.dirname(__file__), 'experiment-results', 'results_' + self.filename[:-4] + 'csv'),
                      sep=',')

    def comparative(self):
        experiment_path = os.path.join(os.path.dirname(__file__), 'experiment-instances', self.filename)
        experiment_scenarios = []
        with open(experiment_path, 'r') as f:
            exp_data = json.load(f)

        for instance in exp_data['instances']:
            experiment_scenarios.append(Solve(instance))

        nature_w = exp_data['algorithms']['nature']['w']
        nature_c1 = exp_data['algorithms']['nature']['c1']
        nature_c2 = exp_data['algorithms']['nature']['c2']
        nature_num_of_particles = exp_data['algorithms']['nature']['num_of_particles']
        nature_max_iter = exp_data['algorithms']['nature']['max_iter']
        results_list = []

        for i, experiment in enumerate(experiment_scenarios):
            repetitions = exp_data['repetitions']
            while repetitions > 0:
                print('Number ' + str(exp_data['repetitions'] - repetitions + 1)
                      + ' repetition of number ' + str(i+1) + ' experiment scenario running...')
                fitness_nature, time_nature = experiment.nature(nature_num_of_particles, nature_max_iter,
                                                                nature_w, nature_c1, nature_c2,
                                                                supress_logs=True)
                fitness_greedy, time_greedy = experiment.greedy(supress_logs=True)

                results_row = [experiment.filename[4:-13], fitness_nature, time_nature, fitness_greedy, time_greedy]
                results_list.append(results_row)

                repetitions -= 1

        df = pd.DataFrame(results_list, columns=['Instance Size', 'Fitness Nature',
                                                 'Time Nature', 'Fitness Greedy', 'Time Greedy'])
        df.to_csv(os.path.join(os.path.dirname(__file__), 'experiment-results',
                               'results_' + self.filename[:-4] + 'csv'), sep=',')