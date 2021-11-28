import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os


def read_instance(filename: str, index_row: bool = True, index_col: bool = False):
    problem_path = os.path.join(os.path.dirname(__file__), 'problem-instances', filename)

    id_row = 0
    if not index_row:
        id_row = None

    id_col = False
    if index_col:
        id_col = 0

    try:
        problem_data = pd.read_csv(problem_path, header=id_row, index_col=id_col)
    except FileNotFoundError:
        print('Error! The file with the provided name does not exist.')
        exit(0)
    except pd.errors.EmptyDataError:
        print('Error! The provided file does not contain data.')
        exit(0)
    except:
        print('Unknown error ocurred!')
        exit(0)

    return problem_data


def display_instance(filename: str, index_row: bool = True, index_col: bool = False, solved: bool = False):
    """
    Displays the problem instance visually. The instance must exist within problem-instances directory
    :param filename: the name of the problem instance
    :param index_row: a flag indicating whether the first row contains headers (default: True)
    :param index_col: a flag indicating whether the first column contains headers (default: False)
    :param solved: a flag indicating whether the solution should be displayed (if available) along with the problem instance (default: False)
    """
    problem_data = read_instance(filename, index_row, index_col)
    # solution_data = read_solution(filename)
    if not isinstance(problem_data, pd.DataFrame):
        print("Error! Data type not valid, quitting...")
    solution_path = os.path.join(os.path.dirname(__file__), 'solved-instances', 'solved_' + filename)

    if solved:
        try:
            solution_data = pd.read_csv(solution_path, header=0)
            if not len(solution_data.columns) == len(problem_data.columns):
                raise AssertionError()
        except FileNotFoundError:
            print('Error! No solution exists for the given problem instance, displaying unsolved.')
            solved = False
        except AssertionError:
            print('Error! The solution size mismatches the problem instance size, displaying unsolved.')
            solved = False

    try:
        graph = nx.Graph(problem_data.values)
    except nx.exception.NetworkXError:
        print("Error! Input data unfit to be displayed as a graph!")
        return

    labeldict = {}
    for i, column in enumerate(problem_data.columns):
        labeldict[i] = str(column)

    if solved:
        for i, color in enumerate(solution_data.values[0]):
            labeldict[i] += ',' + str(color)
        nx.draw(graph, labels=labeldict, with_labels=True,
                # not a very elegant way of scaling the node size but it works
                node_size=[len(label) * len(label) * 60 for _, label in labeldict.items()])
    else:
        nx.draw(graph, labels=labeldict, with_labels=True)

    plt.show()