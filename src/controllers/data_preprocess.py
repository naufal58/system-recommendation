import json
import os
import csv
from nltk import word_tokenize


class DataPreprocess():
    def __init__(self, training_data):
        self.data = training_data

    def get_data(self):
        return self.data

    def replace_missing_symbols(self):
        self.data['soal'] = self.data['soal'].replace(
            '\u201c', "\"").replace('\u2019', '\'').replace('\u201d', "\"")

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

    def get_underlines(self):
        underline = []
        question = word_tokenize(self.data['soal'].replace(
            '.', '').replace(',', '').lower())
        index = 0
        options = ['opt_a', 'opt_b', 'opt_c', 'opt_d']

        for opt in options:
            temp_underline, index = self.option_underline(
                question, self.data[opt], index)
            if len(temp_underline) == 1:
                temp_underline = temp_underline[0]
            underline.append(temp_underline)
        self.data['underline'] = self.convert_list_to_string(underline)

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
        options = ['A', 'B', 'C', 'D']

        for opt in options:
            temp = 'opt_' + opt.lower()
            if self.data['answer'] == opt or self.data['answer'] == self.data[temp]:
                self.data['answer'] = [opt, self.data[temp]]

            if self.data['key_answer'] == opt or self.data['key_answer'] == self.data[temp]:
                self.data['key_answer'] = [opt, self.data[temp]]

        if self.data['answer'] == self.data['key_answer']:
            self.data['result'] = 1
        else:
            self.data['result'] = 0

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

    return True
