import nltk
from nltk import word_tokenize, pos_tag, sent_tokenize, ne_chunk
from nltk.corpus import cmudict
import pandas as pd
import os

class FeatureExtraction():
    def __init__(self, text, underline):
        self.text = text
        self.underline = underline
        self.pronouncing_dict = cmudict.dict()
        self.entries = cmudict.entries()

    def preprocess(self, text):
        return text.replace('.', '').replace(',', '').lower()

    def tag_features(self):
        pos = pos_tag(word_tokenize(self.preprocess(self.text)))
        underlined_postags = []
        irregular_verbs = []
        regular_verbs = []

        for i in range(len(pos)):
            if i in self.underline:
                underlined_postags.append(pos[i])
            if pos[i][1] == 'VBN': ## Irregular verbs 
                irregular_verbs.append(pos[i])
            elif pos[i][1] == 'VBD': ## Regular verbs 
                regular_verbs.append(pos[i])

        return underlined_postags, len(irregular_verbs), len(regular_verbs)

    def check_homophones(self, word):
        list_of_homophones = []
        for i in self.entries:
            if self.pronouncing_dict[word][0] == i[1] and len(list_of_homophones) <= 1 and i[0] != word:
                list_of_homophones.append(i)
                return True, list_of_homophones
        return False, []

    def count_homophones(self):
        """Only check the homophones from the options of the question's answer.
        """
        num_of_homophones = 0
        sentence = word_tokenize(self.preprocess(self.text))
        for i in self.underline:
            try:
                homophones = self.check_homophones(sentence[i])
            except:
                continue
            if homophones[0] == True:
                num_of_homophones += 1
        return num_of_homophones
        
    def syllable_count(self, word):
        vowels = "aeiouy"
        count = 0

        for i in range(len(word)):
            if word[i] in vowels and (i == len(word) - 1 or word[i + 1] not in vowels):
                count += 1

        if word.endswith('e') and count > 1:
            count -= 1

        return max(1, count)

    def flesch_reading_ease(self):
        words = word_tokenize(self.preprocess(self.text))
        sentences = sent_tokenize(self.text)

        total_words = len(words)
        total_sentences = len(sentences)
        total_syllables = sum(self.syllable_count(word) for word in words)

        score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

        return score

    def num_of_conjunctions(self):
        words = word_tokenize(self.preprocess(self.text))
        pos_tags = pos_tag(words)

        conjunctions = [word for word, pos_tag in pos_tags if pos_tag == 'CC']
        return len(conjunctions)

    def tenses_type(self):
        words = word_tokenize(self.preprocess(self.text))
        pos_tags = pos_tag(words)

        future_tense_verbs = []
        past_tense_verbs = []

        for i in range(len(pos_tags)-1):
            current_word, current_pos = pos_tags[i]
            next_word, next_pos = pos_tags[i+1]

            if current_pos == 'MD' and next_pos == 'VB':
                # Check for modal verb 'will' or 'shall' followed by a base form verb
                if current_word.lower() in ['will', 'shall']:
                    future_tense_verbs.append(next_word)
            elif current_pos in ['VBD', 'VBN']:
                past_tense_verbs.append(current_word)
        
        if future_tense_verbs:
            return 'future'
        elif past_tense_verbs:
            return 'past'
        else:
            return 'present'

    def word_frequency(self, word, dictionary, freq_dict):
        i = 0
        stat = 0

        for lemma in dictionary:
            if word == lemma:
                stat = 1
                return freq_dict[i]
                break
            i += 1
        if stat == 0:
            return 0
        
    def difficult_vocab(self):
        path = os.getcwd()
        data_path = path + '/data/lemmas_60k_words.xlsx'
        df = pd.read_excel(data_path, sheet_name='wordfrequency', usecols=['word', 'freq']).astype(str)
        dictionary = df.word.to_list()
        freq_dict = [int(item) for item in df.freq.to_list()]

        difficult_words = []
        for word in word_tokenize(self.preprocess(self.text)):
            freq = self.word_frequency(word, dictionary, freq_dict)
            if freq != 0:
                difficult_words.append({'word': word, 'frequency': self.normalize(freq, 100, max(freq_dict))})
        
        return self.sort_difficult_vocab(difficult_words)

    def sort_difficult_vocab(self, difficult_words):
        sorted_list = sorted(difficult_words, key=lambda x: int(x["frequency"]), reverse=False)
        sum_freq = 0
        for word_freq in sorted_list:
            sum_freq += word_freq['frequency']
        sum_freq = format(sum_freq/len(sorted_list), '.3f')
        return float(sum_freq)

    def normalize(self, value, min_value, max_value):
        return (value - min_value) / (max_value - min_value)
    