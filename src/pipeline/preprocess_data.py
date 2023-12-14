from src.controllers.data_preprocess import DataPreprocess, convert_to_json
import os
import json


def get_training_data(filename):
    path = os.path.join(os.getcwd(), 'data')
    data_path = os.path.join(path, filename + '.json')

    with open(data_path, 'r') as training_file:
        training_data = json.load(training_file)
    return training_data


def set_training_data(filename, data):
    path = os.path.join(os.getcwd(), 'data')
    data_path = os.path.join(path, filename + '.json')
    with open(data_path, 'w') as f:
        json.dump(data, f, indent=4)
    return True


def preprocess_pipeline(filename, full_pipeline=False):
    training_data = []
    if convert_to_json(filename):
        data_files = get_training_data(filename)
        for data in data_files:
            processed_data = DataPreprocess(data)
            processed_data.replace_missing_symbols()
            processed_data.get_underlines()
            processed_data.check_answer_result()
            training_data.append(processed_data.get_data())
        if full_pipeline:
            return training_data
        elif set_training_data(filename, training_data):
            return True
    return False
