from src.controllers.feature_extraction import FeatureExtraction

def extract_features(text, underline):
    question_characteristics = FeatureExtraction(text, underline)
    response = {}
    response['question_text'] = text

    print('Getting tense type...')
    response['tense_type'] = question_characteristics.tenses_type()

    print('Getting tags features...')
    response['underlined_postags'], response['irregular_verbs'], response['regular_verbs'] = question_characteristics.tag_features()

    print('Counting homophones...')
    response['homophones'] = question_characteristics.count_homophones()

    print('Counting conjunctions...')
    response['conjunctions'] = question_characteristics.num_of_conjunctions()

    print('Calculating Flesch Reading Ease...')
    response['flesch_reading_ease'] = question_characteristics.flesch_reading_ease()

    print('Calculating vocabulary difficulty...')
    response['vocabulary_difficulty_score'] = question_characteristics.difficult_vocab()

    return response
