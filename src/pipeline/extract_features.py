from src.controllers.feature_extraction import FeatureExtraction
from src.utils.helper_functions import get_training_data, preprocess_underlined, set_training_data

def extract_features(text, underline, data, essential_features_only=False):
    question_characteristics = FeatureExtraction(text, underline, data)
    response = {}
    question_characteristics.get_key_index()
    # if essential_features_only == False:
    #     response['question_text'] = text
    #     response['underlined_postags'], response['irregular_verbs'], response['regular_verbs'] = question_characteristics.tag_features()
    # else:
    #     _, response['irregular_verbs'], response['regular_verbs'] = question_characteristics.tag_features()

    response['tense_type'] = question_characteristics.tenses_type()

    # temp_homophones = question_characteristics.count_homophones()
    # if temp_homophones[0]:
    #     response['key_is_homophone'] = 'key_is_homophone'
    # if temp_homophones[1]:
    #     response['answer_is_homophone'] = 'answer_is_homophone'

    response['conjunctions'] = question_characteristics.num_of_conjunctions()

    response['error_type'] = question_characteristics.error_type()

    response['flesch_reading_ease'] = question_characteristics.flesch_reading_ease()

    response['vocabulary_difficulty_score'] = question_characteristics.difficult_vocab()
    response['result'] = data['result']

    return response

def extract_from_file(filename):
    training_data = get_training_data(filename)
    data_extract = []
    print('Starting pipeline...')
    for data in training_data:
        data_extract.append(extract_features(data['soal'], preprocess_underlined(data['underline']), data, essential_features_only=True))
    set_training_data({'data': data_extract}, filename)
    print(f'Data questions from {filename} file has been extracted.')
    return {'msg': f'Data questions from {filename} file has been extracted.'}
