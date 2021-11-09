import networkx as nx
import matplotlib.pyplot as plt
import networkx.exception
import pandas as pd
import fire
import os


def display_instance(filename: str, index_row: bool = True, index_col: bool = False):
    """
    Displays the problem instance visually. The instance must exist within problem-instances directory
    :param filename: the name of the problem instance
    :param index_row: a flag indicating whether the first row contains headers (default: True)
    :param index_col: a flag indicating whether the first column contains headers (default: False)
    """
    path = os.path.join(os.path.dirname(__file__), 'problem-instances', filename)

    id_row = 0
    if not index_row:
        id_row = None

    id_col = False
    if index_col:
        id_col = 0

    try:
        input_data = pd.read_csv(path, header=id_row, index_col=id_col)
    except FileNotFoundError:
        print('Error! The file with the provided name does not exist.')
        return
    except pd.errors.EmptyDataError:
        print('Error! The provided file does not contain data.')
        return
    except:
        print('Unknown error ocurred!')
        return

    try:
        graph = nx.Graph(input_data.values)
    except networkx.exception.NetworkXError:
        print("Error! Input data unfit to be displayed as a graph!")
        return

    labeldict = {}
    for i, column in enumerate(input_data.columns):
        labeldict[i] = column

    nx.draw(graph, labels=labeldict, with_labels=True)
    plt.show()


if __name__ == '__main__':
    fire.Fire({
        "display": display_instance
    })

    # display_instance('size11_instance.csv', index_col=False)
    # display_instance('size3_instance.csv', index_row=False)
    # display_instance('size1_instance.csv', index_row=False)