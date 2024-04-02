from src.controllers.discretization import Discretization
from src.utils.helper_functions import get_training_data, set_training_data

def start(filename, training_data=False, full_pipeline=False):
    if not full_pipeline:
        feature_data = get_training_data(filename)['data']
    else:
        feature_data = training_data
    discrete_data = Discretization(feature_data)
    new_data = discrete_data.remove_correct_answers()
    set_training_data(new_data, filename)
    return new_data