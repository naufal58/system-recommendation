from src.controllers.feature_extraction import FeatureExtraction
from src.utils.helper_functions import get_training_data, preprocess_key_answer, set_training_data
import nltk
import ast
import time
# import pd as pandas

nltk.download('cmudict')

def extract_features(soal, opt_a, opt_b, opt_c, opt_d, answer, key_answer_text, data, essential_features_only=False ):
    question_characteristics = FeatureExtraction(soal, opt_a, opt_b, opt_c, opt_d, answer, key_answer_text, data)
    response = {}

    gerund_req, gerund_phrase_req = question_characteristics.gerund_requirement()
    irregular_past, past_participle = question_characteristics.irregular_past_form()
    singular_expression, plural_expression = question_characteristics.noncount_noun_expression()

    response['nama'] = data['nama']
    response['soal'] = data['soal']

    response['infinitive_requirement'] = question_characteristics.infinitive_requirement()
    response['gerund_requirement'] = gerund_req
    response['gerund_phrase_requirement'] = gerund_phrase_req
    response['irregular_past_form'] = irregular_past
    response['past_participle'] = past_participle
    response['relative_pronouns'] = question_characteristics.relative_pronouns()
    response['singular_expression'] = singular_expression
    response['plural_expression'] = plural_expression
    response['factual_conditional'] = question_characteristics.factual_conditional()
    response['importance_subjunctive_verb'] = question_characteristics.importance_subjunctive_verb()
    # question_characteristics.get_key_index()
    # if essential_features_only == False:
    #     response['question_text'] = text
    #     response['underlined_postags'], response['irregular_verbs'], response['regular_verbs'] = question_characteristics.tag_features()
    # else:
    #     _, response['irregular_verbs'], response['regular_verbs'] = question_characteristics.tag_features()

    # response['tense_type'] = question_characteristics.tenses_type()
    # response['subject_verb_agreement'] = question_characteristics.check_subject_verb_agreement()

    # temp_homophones = question_characteristics.count_homophones()
    # if temp_homophones[0]:
    #     response['key_is_homophone'] = 'key_is_homophone'
    # if temp_homophones[1]:
    #     response['answer_is_homophone'] = 'answer_is_homophone'

    # response['conjunctions'] = question_characteristics.num_of_conjunctions()

    # response['error_type'] = question_characteristics.error_type()

    # response['flesch_reading_ease'] = question_characteristics.flesch_reading_ease()

    # response['vocabulary_difficulty_score'] = question_characteristics.difficult_vocab()
    response['result'] = data['result']

    return response

def extract_from_file(filename, full_pipeline=False):
    start_time = time.time()

    training_data = get_training_data(filename)
    data_extract = []
    print('Starting pipeline...')
    for data_item in training_data:
        if isinstance(data_item, list) and len(data_item) == 1 and isinstance(data_item[0], dict):
            data = data_item[0]  
            option_label = data['key_answer'][0].lower()
            correct_option_text = data[f'opt_{option_label}']
            key_answer_processed = preprocess_key_answer(data['key_answer'])
            features = extract_features(data['soal'], data['opt_a'], data['opt_b'], data['opt_c'], data['opt_d'], correct_option_text, key_answer_processed, data, essential_features_only=True)
            data_extract.append(features)
        else:
            print(f"Error: Data item is not a properly structured dictionary: {data_item}")
            continue

    set_training_data({'data': data_extract}, filename)
    # dict = json.loads(data)
    # df = json_normalize(dict['data']) 


    end_time = time.time()  # End timing
    runtime = end_time - start_time  # Calculate total runtime
    print(f"Runtime: {runtime}")

    if full_pipeline:
        return data_extract
    return {'msg': f'Data questions from {filename} file has been extracted.'}


def full_extraction_pipeline(training_data):
    data_extract = []
    for data in training_data:
        data_extract.append(extract_features(data['soal'], preprocess_underlined(data['underline']), data, essential_features_only=True))
    return data_extract
