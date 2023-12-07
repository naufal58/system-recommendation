import json
import os
import random
import string
 
def random_string(n):
    res = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=n))
 
    return res

def get_training_data(filename = "training_data"):
    path = os.path.join(os.getcwd(), 'data')
    data_path = os.path.join(path, filename + '.json')

    with open(data_path, 'r') as training_file:
        training_data = json.load(training_file)
    return training_data

def set_training_data(data, filename):
    path = os.getcwd()
    suffix = ".json"
    data_path = path + "/data/" + filename + suffix

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

def has_answer_only(training_data):
    new_data = []
    for data in training_data:
        if data['answer'] != None:
            new_data.append(data)
    return new_data
