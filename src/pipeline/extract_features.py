from src.controllers.feature_extraction import FeatureExtraction
from src.utils.helper_functions import get_training_data, preprocess_underlined, set_training_data

def extract_features(text, underline, essential_features_only=False):
    question_characteristics = FeatureExtraction(text, underline)
    response = {}
    print('Getting tags features...')
    if essential_features_only == False:
        response['question_text'] = text
        response['underlined_postags'], response['irregular_verbs'], response['regular_verbs'] = question_characteristics.tag_features()
    else:
        _, response['irregular_verbs'], response['regular_verbs'] = question_characteristics.tag_features()

    print('Getting tense type...')
    response['tense_type'] = question_characteristics.tenses_type()

    print('Counting homophones...')
    response['homophones'] = question_characteristics.count_homophones()

    print('Counting conjunctions...')
    response['conjunctions'] = question_characteristics.num_of_conjunctions()

    print('Calculating Flesch Reading Ease...')
    response['flesch_reading_ease'] = question_characteristics.flesch_reading_ease()

    print('Calculating vocabulary difficulty...')
    response['vocabulary_difficulty_score'] = question_characteristics.difficult_vocab()

    return response

def extract_from_file(filename):
    training_data = get_training_data(filename)
    data_extract = []
    for data in training_data:
        data_extract.append(extract_features(data['soal'], preprocess_underlined(data['underline']), essential_features_only=True))
    set_training_data({'data': data_extract})

    return {'msg': f'Data questions from {filename} file has been extracted.'}
