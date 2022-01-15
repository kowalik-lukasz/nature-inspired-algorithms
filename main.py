import fire
from algorithms import Solve
from experiments import Experiment
from utils import display_instance, generate_instance


if __name__ == '__main__':
    fire.Fire({
        "display": display_instance,
        "generate": generate_instance,
        "solve": Solve,
        "experiment": Experiment
    })

    # display_instance('size11_instance.csv', index_col=True, solved=True)
    # display_instance('size3_instance.csv', index_row=False, solved=True)
    # display_instance('size1_instance.csv', index_row=False)