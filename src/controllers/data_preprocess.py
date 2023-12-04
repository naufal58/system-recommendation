import json
import os
import csv
from nltk import word_tokenize

class DataPreprocess():
    def __init__(self, filename):
        self.filename = filename
        self.data_path = os.path.join(os.getcwd(), 'data')
        self.json_data_path = os.path.join(self.data_path, self.filename + '.json')

    def convert_to_json(self):
        path = os.path.join(os.getcwd(), 'data')
        data_path = os.path.join(path, self.filename + '.csv')
        csv_data = []

        with open(data_path, 'r', encoding='utf-8', errors='replace') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                csv_data.append(row)

        json_filename = self.filename + '.json'
        data_path = os.path.join(path, json_filename)

        # Write the data to a JSON file
        with open(data_path, 'w') as json_file:
            json.dump(csv_data, json_file, indent=4)

        print(f"Conversion complete. Data written to {json_filename}")
        return True
    
    def get_training_data(self):
        path = os.path.join(os.getcwd(), 'data')
        data_path = os.path.join(path, self.filename + '.json')

        with open(data_path, 'r') as training_file:
            training_data = json.load(training_file)
        return training_data

    def replace_missing_symbols(self):
        training_data = self.get_training_data()
        for data in training_data:
            data['soal'] = data['soal'].replace('\u201c', "\"").replace('\u2019', '\'').replace('\u201d', "\"")

        with open(self.json_data_path, 'w') as f:
            json.dump(training_data, f, indent=4)
        return True
    
    def get_underlines(self):
        training_data = self.get_training_data()
        for data in training_data:
            underline = []
            question = word_tokenize(data['soal'].replace('.', '').replace(',', '').lower())
            index = 0
            options = ['opt_a', 'opt_b', 'opt_c', 'opt_d']
            for opt in options:
                temp_underline, index = self.option_underline(question, data[opt], index)
                if len(temp_underline) == 1:
                    temp_underline = temp_underline[0]
                underline.append(temp_underline)
            data['underline'] = underline
        with open(self.json_data_path, 'w') as f:
            json.dump(training_data, f, indent=4)
        return True
    
    def option_underline(self, question, option, index):
        underline = []
        check = 0
        while check != len(option.split(' ')):
            for word in option.split(' '):
                while index != len(question):
                    if word == question[index]:
                        underline.append(index)
                        check += 1
                        break
                    index += 1
        return underline, index
    
    def check_answer_result(self):
        training_data = self.get_training_data()
        for data in training_data:
            if data['answer'] == data['key_answer']:
                data['result'] = 1
            else:
                data['result'] = 0

            if data['answer'] == 'A':
                data['answer'] = ['A', data['opt_a']]
            elif data['answer'] == 'B':
                data['answer'] = ['B', data['opt_b']]
            elif data['answer'] == 'C':
                data['answer'] = ['C', data['opt_c']]
            elif data['answer'] == 'D':
                data['answer'] = ['D', data['opt_d']]

            if data['key_answer'] == 'A':
                data['key_answer'] = ['A', data['opt_a']]
            elif data['key_answer'] == 'B':
                data['key_answer'] = ['B', data['opt_b']]
            elif data['key_answer'] == 'C':
                data['key_answer'] = ['C', data['opt_c']]
            elif data['key_answer'] == 'D':
                data['key_answer'] = ['D', data['opt_d']]
        with open(self.json_data_path, 'w') as f:
            json.dump(training_data, f, indent=4)
        return True
