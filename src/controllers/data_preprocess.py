import json
import os
import csv
import re
from nltk import word_tokenize

class DataPreprocess():
    def __init__(self, training_data):
        if isinstance(training_data, list) and all(isinstance(i, dict) for i in training_data):
            self.data = training_data
        else:
            raise ValueError("training_data must be a list of dictionaries")
    
    def get_data(self):
        return self.data

    def replace_missing_symbols(self):
        for data_dict in self.data:
            if 'soal' in data_dict and isinstance(data_dict['soal'], str):
                data_dict['soal'] = data_dict['soal'].replace('\u201c', '\"').replace('\u2019', '\'').replace('\u201d', '\"')
        return True
    
    def convert_list_to_string(self, input_list):
        result_string = ""
        
        for sublist in input_list:
            if isinstance(sublist, list):
                if len(sublist) == 2:
                    result_string += f"{sublist[0]}-{sublist[1]},"
                else:
                    result_string += ",".join(map(str, sublist))
                    result_string += ","
            else:
                result_string += f"{sublist},"
        
        result_string = result_string.rstrip(',')
        
        return result_string

    def complete_sentences(self):
        options = ['A', 'B', 'C', 'D']
        for data_dict in self.data:
            for opt in options:
                option_key = f'opt_{opt.lower()}'
                if data_dict.get('answer') == opt:
                    data_dict['answer'] = [opt, data_dict[option_key]]
                if data_dict.get('key_answer') == opt:
                    data_dict['key_answer'] = [opt, data_dict[option_key]]

            # Fill in the blanks for the sentence in 'soal'
            correct_option_key = f'opt_{data_dict.get("key_answer", [""])[0].lower()}'
            if correct_option_key in data_dict:
                correct_answer = data_dict[correct_option_key]
                data_dict['soal'] = data_dict['soal'].replace('_________', correct_answer)

        return True
    
    def check_answer_result(self):
        for data_dict in self.data:

            if data_dict['answer'] == data_dict['key_answer'][1]:
                data_dict['result'] = 1
            else:
                data_dict['result'] = 0
        return True

def convert_to_json(filename):
    path = os.path.join(os.getcwd(), 'data')
    data_path = os.path.join(path, filename + '.csv')
    csv_data = []

    with open(data_path, 'r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    json_filename = filename + '.json'
    data_path = os.path.join(path, json_filename)

    # Write the data to a JSON file
    with open(data_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=4)

    print(f"Conversion complete. Data written to {json_filename}")
    return True
