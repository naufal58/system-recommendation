import json
import os
from pipeline.demo import DemoPipeline

def get_training_data():
    path = os.getcwd()
    data_path = path + '/data/training_data.json'

    with open(data_path, 'r') as training_file:
        training_data = json.load(training_file)
    return training_data

def set_training_data(data):
    path = os.getcwd()
    data_path = path + '/data/new_training_data.json'

    try:
        with open(data_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return True
    except:
        return False

def preprocess_underlined(underline):
    underline_list = []
    for i in underline.split(','):
        underline_list.append(int(i.split('-')[0]))
    return underline_list

def demo_extract():
    training_data = get_training_data()
    new_training_data = []
    for data in training_data['data']:
        demo_pipeline = DemoPipeline(data['text'], preprocess_underlined(data['underline']))
        # print(demo_pipeline.pipeline())
        new_training_data.append(demo_pipeline.pipeline())
        if data['id'] == 1:
            break
    if set_training_data({'data': new_training_data}):
        return True
    else:
        return False
    # demo_pipeline = DemoPipeline("It's always a good idea to seek shelter from the evil gaze of the sun.")

