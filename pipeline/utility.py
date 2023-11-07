import json
import os
from pipeline.demo import DemoPipeline

def get_training_data():
    path = os.getcwd()
    data_path = path + '/data/training_data.json'

    with open(data_path, 'r') as training_file:
        training_data = json.load(training_file)
    return training_data

def preprocess_underlined(underline):
    underline_list = []
    for i in underline.split(','):
        underline_list.append(int(i.split('-')[0]))
    return underline_list

def demo_extract():
    training_data = get_training_data()
    for data in training_data['data']:
        demo_pipeline = DemoPipeline(data['text'], preprocess_underlined(data['underline']))
        print(demo_pipeline.pipeline())
        if data['id'] == 5:
            break
    return True
    # demo_pipeline = DemoPipeline("It's always a good idea to seek shelter from the evil gaze of the sun.")

