from src.controllers.discretization import Discretization
from src.utils.helper_functions import get_training_data, set_training_data

def start(filename):
    print(f"Starting discretization pipeline on '{filename}.json'...")
    feature_data = get_training_data(filename)
    discrete_data = Discretization(feature_data['data'])
    discrete_data.normalize_numeric()
    new_data = discrete_data.remove_correct_answers()
    set_training_data(new_data, filename)
    return True