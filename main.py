import networkx as nx
import matplotlib.pyplot as plt
import networkx.exception
import pandas as pd
import fire
import os


def solve(filename: str, index_row: bool = True, index_col: bool = False):
    """
    Displays the problem instance visually. The instance must exist within problem-instances directory
    :param filename: the name of the problem instance
    :param index_row: a flag indicating whether the first row contains headers (default: True)
    :param index_col: a flag indicating whether the first column contains headers (default: False)
    """
    pass


def display_instance(filename: str, index_row: bool = True, index_col: bool = False, solved: bool = False):
    """
    Displays the problem instance visually. The instance must exist within problem-instances directory
    :param filename: the name of the problem instance
    :param index_row: a flag indicating whether the first row contains headers (default: True)
    :param index_col: a flag indicating whether the first column contains headers (default: False)
    :param solved: a flag indicating whether the solution should be displayed (if available) along with the problem instance (default: False)
    """
    problem_path = os.path.join(os.path.dirname(__file__), 'problem-instances', filename)
    solution_path = os.path.join(os.path.dirname(__file__), 'solved-instances', 'solved_' + filename)

    id_row = 0
    if not index_row:
        id_row = None

    id_col = False
    if index_col:
        id_col = 0

    try:
        input_data = pd.read_csv(problem_path, header=id_row, index_col=id_col)
    except FileNotFoundError:
        print('Error! The file with the provided name does not exist.')
        return
    except pd.errors.EmptyDataError:
        print('Error! The provided file does not contain data.')
        return
    except:
        print('Unknown error ocurred!')
        return

    if solved:
        try:
            solution_data = pd.read_csv(solution_path, header=0)
            if not len(solution_data.columns) == len(input_data.columns):
                raise AssertionError()
        except FileNotFoundError:
            print('Error! No solution exists for the given problem instance, displaying unsolved.')
            solved = False
        except AssertionError:
            print('Error! The solution size mismatches the problem instance size, displaying unsolved.')
            solved = False

    try:
        graph = nx.Graph(input_data.values)
    except networkx.exception.NetworkXError:
        print("Error! Input data unfit to be displayed as a graph!")
        return

    labeldict = {}
    for i, column in enumerate(input_data.columns):
        labeldict[i] = str(column)

    if solved:
        for i, color in enumerate(solution_data.values[0]):
            labeldict[i] += ',' + str(color)
        nx.draw(graph, labels=labeldict, with_labels=True,
                node_size=[len(label) * 200 for _, label in labeldict.items()])
    else:
        nx.draw(graph, labels=labeldict, with_labels=True)

    plt.show()


if __name__ == '__main__':
    fire.Fire({
        "display": display_instance
    })

    display_instance('size11_instance.csv', index_col=True, solved=True)
    # display_instance('size3_instance.csv', index_row=False, solved=True)
    # display_instance('size1_instance.csv', index_row=False)