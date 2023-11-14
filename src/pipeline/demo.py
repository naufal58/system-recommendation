from src.controllers.feature_extraction import *

class DemoPipeline:
    def __init__(self, text, underline):
        self.text = text
        self.underline = underline
    
    def get_homophones(self):
        homophones = count_homophones(self.text)
        return homophones
    
    def get_conjunctions(self):
        conjunctions = num_of_conjunctions(self.text)
        return conjunctions
    
    def get_tense_type(self):
        tense_type = tenses_type(self.text)
        return tense_type
    
    def get_fre(self):
        fre = flesch_reading_ease(self.text)
        return fre
    
    def get_tag_features(self):
        underlined_postags, irregular_verbs, regular_verbs = tag_features(self.text, self.underline)
        return underlined_postags, irregular_verbs, regular_verbs
    
    def get_vocab_difficulty(self):
        diff_vocab = difficult_vocab(self.text)
        return diff_vocab
    
    def pipeline(self):
        response = {}
        response['question_text'] = self.text

        print('Getting tense type...')
        response['tense_type'] = self.get_tense_type()

        print('Getting tags features...')
        response['underlined_postags'], response['irregular_verbs'], response['regular_verbs'] = self.get_tag_features()

        print('Counting homophones...')
        response['homophones'] = self.get_homophones()

        print('Counting conjunctions...')
        response['conjunctions'] = self.get_conjunctions()

        print('Calculating Flesch Reading Ease...')
        response['flesch_reading_ease'] = self.get_fre()

        print('Calculating vocabulary difficulty...')
        response['difficult_vocab'] = self.get_vocab_difficulty()

        return response
