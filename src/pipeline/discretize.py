from src.controllers.discretization import Discretization
from src.utils.helper_functions import get_training_data, set_training_data

def start(filename):
    print(f"Starting discretization pipeline on '{filename}.json'...")
    feature_data = get_training_data(filename)
    discrete_data = Discretization(feature_data['data'])
    discrete_data.normalize_numeric()
    # discrete_data.discrete_categorical()
    set_training_data(feature_data, filename)
    return True