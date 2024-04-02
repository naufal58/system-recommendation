from src.controllers.data_preprocess import DataPreprocess, convert_to_json
import os
import json
import ast
import time

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
    start_time = time.time()
    print(start_time)
    training_data = []
    if convert_to_json(filename):
        data_files = get_training_data(filename)
        for data_item in data_files:
            if isinstance(data_item, str):
                try:
                    data_dict = ast.literal_eval(data_item.replace("'", "\""))
                except ValueError as e:
                    print(f"Error converting data to dictionary: {e}")
                    continue
            elif isinstance(data_item, dict):
                data_dict = data_item
            else:
                continue
            processed_data = DataPreprocess([data_dict])
            processed_data.replace_missing_symbols()
            processed_data.complete_sentences()
            processed_data.check_answer_result()
            training_data.append(processed_data.get_data())
        if full_pipeline:
            return training_data
        elif set_training_data(filename, training_data):
            return True
    end_time = time.time()  # End timing
    runtime = end_time - start_time  # Calculate total runtime\
    print(runtime)
    return False
