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

def set_training_data(data):
    path = os.getcwd()
    filename = random_string(5) + ".json"
    data_path = path + "/data/" + filename

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
