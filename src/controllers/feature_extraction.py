import nltk
from nltk import word_tokenize, pos_tag, sent_tokenize, ne_chunk
from nltk.corpus import cmudict
import pandas as pd
import os
import spacy

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class FeatureExtraction():
    def __init__(self, soal, opt_a, opt_b, opt_c, opt_d, answer, key_answer, data):
        self.soal = soal
        self.key_answer = key_answer.lower()
        self.answer = answer.lower()
        self.pronouncing_dict = cmudict.dict()
        self.entries = cmudict.entries()
        self.data = data
        self.options = {'a': opt_a, 'b': opt_b, 'c': opt_c, 'd': opt_d}
        self.nlp = spacy.load("en_core_web_sm")
        self.pos_tags, self.named_entities = self.preprocess()


    def preprocess(self):
        soal = self.soal.replace('.', '').replace(',', '').lower()
        key_answer = self.key_answer.replace('.', '').replace(',', '').lower()
        tokens = word_tokenize(self.soal)
        # Get POS tags for the tokens
        pos_tags = pos_tag(tokens)
        # Named Entity Recognition
        named_entities = ne_chunk(pos_tags)
        return pos_tags, named_entities

    def tokenize_and_tag_options(self):
        options_tags = {}
        for key, option_text in self.options.items():
            phrase_tokens = word_tokenize(option_text)
            phrase_pos_tags = pos_tag(phrase_tokens)
            options_tags[key] = phrase_pos_tags
        return options_tags

    def relative_pronouns(self):
        relative_pronouns = {'who', 'whose', 'whom', 'which', 'that'}
        found_in_sentence = False
        
        for token in self.nlp(self.soal.lower()):
            print(f"Token: {token.text}, POS: {token.pos_}, Tag: {token.tag_}")
            if token.lower_ in relative_pronouns:
                if token.dep_ in ('nsubj', 'dobj', 'pobj', 'attr', 'nsubjpass'):
                    found_in_sentence = True
                    print(f"Found relative pronoun in sentence: {token.text} as {token.dep_}")
                    break
        # Check all options            
        if not found_in_sentence:
            print("Checking options for relative pronouns...")
            for option_key, option_text in self.options.items():
                for token in self.nlp(option_text.lower()):
                    if token.lower_ in relative_pronouns:
                        print(f"Found relative pronoun in options ({option_key}): {token.text}")
                        return True 
    
        return found_in_sentence

    def importance_subjunctive_verb(self):
        # Parse the sentence using spaCy
        doc = self.nlp(self.soal)
        subjunctive_verbs = {
            "suggest", "recommend", "demand", "request", "ask", "propose", "advise", "urge", "require", 
            "insist", "vital", "prefer", "order", "command", "desire", "imperative", "important", 
            "necessary", "essential", "crucial", "urge", "hope", "dictate", "mandate", "recommendation",
            "advocate", "ask", "stipulate", "condition", "wish", "if only", "would rather", "recommendation",
            "necessitate", "expect", "want", "decree", "instruct", "implore", "permit", "allow", "advise", 
            "encourage", "forbid", "prohibit", "express a desire", "express a preference", "express a wish"
        }

        tokens = word_tokenize(self.soal)
        pos_tags = pos_tag(tokens)

        for i, token in enumerate(doc):
            if token.lemma_ in subjunctive_verbs and i + 1 < len(tokens) and tokens[i + 1] == "that":
                for j in range(i + 1, len(tokens)):
                    if tokens[j].lower() == self.key_answer:
                        return True
        return False

    def factual_conditional(self):
        tokens = word_tokenize(self.soal)
        pos_tags = pos_tag(tokens)

        # Find if
        if_index = None
        modal_detected = False
        for i, (word, tag) in enumerate(pos_tags):

            if word.lower() == "if":
                if_index = i
            
            # After if find MD
            elif if_index is not None and tag == 'MD':
                modal_detected = True
            
            # Check MD followed by VB
            elif modal_detected and tag == 'VB':
                return True
                factual_condition = True
            
        phrase_tokens = word_tokenize(self.answer)
        phrase_pos_tags = pos_tag(phrase_tokens)
        
        if len(phrase_pos_tags) > 1 and phrase_pos_tags[0][1] == 'MD' and phrase_pos_tags[1][1] == 'VB':
            return True

        return False

    def irregular_past_form(self):
        doc_sentence = self.nlp(self.soal.lower())
        
        irregular_past = False
        past_participle = False

        for token in doc_sentence:
            print(f"Token: {token.text}, Tag: {token.tag_}, Lemma: {token.lemma_}")
            if token.tag_ in ["VBD", "VBN"]:
                if token.text != token.lemma_ and not token.text.endswith('ed'):
                    irregular_past = True
                    print(f"Found irregular past form: {token.text}")

        need_to_check_options = not irregular_past or not past_participle
        
        # Check all options
        if need_to_check_options:
            for key, option_text in self.options.items():
                doc_option = self.nlp(option_text.lower())
                for token in doc_option:
                    print(f"Option [{key}]: Token: {token.text}, Tag: {token.tag_}, Lemma: {token.lemma_}")
                    if token.tag_ in ["VBD", "VBN"]:
                        if token.text != token.lemma_ and not token.text.endswith('ed'):
                            irregular_past = True
                            print(f"Found irregular past form in options [{key}]: {token.text}")
                        elif token.text.endswith('ed'):
                            past_participle = True
                            print(f"Found past participle in options [{key}]: {token.text}")

        print(f"Final result - Irregular past: {irregular_past}, Past participle: {past_participle}")
        return irregular_past, past_participle

    def infinitive_requirement(self):
        options_tags = self.tokenize_and_tag_options()

        tokens = word_tokenize(self.soal)
        pos_tags = pos_tag(tokens)

        infinitive_found_in_sentence = False

        for i, (word, tag) in enumerate(pos_tags[:-1]):
            if word == "to" and pos_tags[i + 1][1] == 'VB':
                infinitive_phrase = f"{word} {tokens[i + 1]}"
                if infinitive_phrase == self.key_answer or infinitive_phrase == self.answer:
                    return True
                infinitive_found_in_sentence = True

        # Check all options
        if not infinitive_found_in_sentence:
            for option_key, option_text in self.options.items():
                phrase_tokens = word_tokenize(option_text)
                phrase_pos_tags = pos_tag(phrase_tokens)
                if len(phrase_tokens) > 1 and phrase_tokens[0] == "to" and phrase_pos_tags[1][1] == 'VB':
                    return True
        return False

    def gerund_requirement(self):
        options_tags = self.tokenize_and_tag_options()
        
        gerund_requirement = False
        gerund_phrase_requirement = False

        # First, scan the sentence for gerunds and gerund phrases
        tokens = word_tokenize(self.soal)
        pos_tags = pos_tag(tokens)

        for i, (token, tag) in enumerate(pos_tags):
            if tag == 'VBG':
                if token == self.key_answer or token == self.answer:
                    # Check for gerund
                    if i == 0 or (i > 0 and pos_tags[i-1][1] not in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
                        gerund_requirement = True
                    # Check for a gerund phrase
                    elif i > 0 and pos_tags[i-1][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and pos_tags[i-1][0] != "to":
                        gerund_phrase_requirement = True

        # Check all options
        if not gerund_requirement and not gerund_phrase_requirement:
            for option_key, option_text in self.options.items():
                phrase_tokens = word_tokenize(option_text)
                phrase_pos_tags = pos_tag(phrase_tokens)
                if phrase_pos_tags and phrase_pos_tags[0][1] == 'VBG':
                    gerund_requirement = True
                    if len(phrase_tokens) > 1 and any(tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] for _, tag in phrase_pos_tags[1:]):
                        gerund_phrase_requirement = True
                    break

        return gerund_requirement, gerund_phrase_requirement

    def noncount_noun_expression(self):
        tokens = word_tokenize(self.soal)
        pos_tags = pos_tag(tokens)

        singular_expression = False
        plural_expression = False

        # Enhanced checks for singular and plural expressions
        for i, (word, tag) in enumerate(pos_tags):
            # Check for singular expressions
            if tag == 'DT' and word in ['a', 'an', 'the']:
                if i + 1 < len(pos_tags) and pos_tags[i + 1][1] in ['NN', 'NNP']:  # Singular noun or proper noun
                    singular_expression = True

            # Check for plural expressions
            elif tag in ['CD', 'DT'] and word in ['some', 'many', 'several', 'few', 'more']:
                if i + 1 < len(pos_tags) and pos_tags[i + 1][1] in ['NNS', 'NNPS']:  # Plural noun or proper noun plural
                    plural_expression = True
            elif tag == 'NNS' or tag == 'NNPS':  # Directly identifying plural nouns
                plural_expression = True

            # Enhanced detection for uncountable or mass nouns which can be tricky
            # Typically, mass nouns would not use 'a' or 'an' but can be detected by certain quantifiers or contexts
            elif word in ['much', 'little', 'a lot of', 'lots of', 'a large amount of', 'a great deal of']:
                singular_expression = True  # These can imply singular mass nouns

            elif word in ['a number of', 'the number of', 'quantities of', 'numbers of']:
                plural_expression = True  # These imply plural or collective amounts

        return singular_expression, plural_expression
        

    # def tag_features(self):
    #     pos = pos_tag(word_tokenize(self.preprocess(self.text)))
    #     underlined_postags = []
    #     irregular_verbs = []
    #     regular_verbs = []

    #     for i in range(len(pos)):
    #         if i in self.underline:
    #             underlined_postags.append(pos[i])
    #         if pos[i][1] == 'VBN': ## Irregular verbs 
    #             irregular_verbs.append(pos[i])
    #         elif pos[i][1] == 'VBD': ## Regular verbs 
    #             regular_verbs.append(pos[i])
    #     return underlined_postags, len(irregular_verbs), len(regular_verbs)

    # def check_homophones(self, word):
    #     list_of_homophones = []
    #     for i in self.entries:
    #         if self.pronouncing_dict[word][0] == i[1] and len(list_of_homophones) <= 1 and i[0] != word:
    #             list_of_homophones.append(i)
    #             return True, list_of_homophones
    #     return False, []

    # def count_homophones(self):
    #     """Only check the homophones from the question's answer and answer key.
    #     """
    #     try:
    #         homophones_ans_key = self.check_homophones(self.data['key_answer'][1])
    #         homophones_ans = self.check_homophones(self.data['answer'][1])
    #     except:
    #         return False, False
    #     return [homophones_ans_key[0], homophones_ans[0]]
        
    # def syllable_count(self, word):
    #     vowels = "aeiouy"
    #     count = 0

    #     for i in range(len(word)):
    #         if word[i] in vowels and (i == len(word) - 1 or word[i + 1] not in vowels):
    #             count += 1

    #     if word.endswith('e') and count > 1:
    #         count -= 1

    #     return max(1, count)

    # def flesch_reading_ease(self):
    #     words = word_tokenize(self.preprocess(self.text))
    #     sentences = sent_tokenize(self.text)

    #     total_words = len(words)
    #     total_sentences = len(sentences)
    #     total_syllables = sum(self.syllable_count(word) for word in words)

    #     score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

    #     return score

    # def num_of_conjunctions(self):
    #     words = word_tokenize(self.preprocess(self.text))
    #     pos_tags = pos_tag(words)

    #     conjunctions = [word for word, pos_tag in pos_tags if pos_tag == 'CC']
    #     return len(conjunctions)

    # def tenses_type(self):
    #     words = word_tokenize(self.preprocess(self.text))
    #     pos_tags = pos_tag(words)

    #     future_tense_verbs = []
    #     past_tense_verbs = []

    #     for i in range(len(pos_tags)-1):
    #         current_word, current_pos = pos_tags[i]
    #         next_word, next_pos = pos_tags[i+1]

    #         if current_pos == 'MD' and next_pos == 'VB':
    #             # Check for modal verb 'will' or 'shall' followed by a base form verb
    #             if current_word.lower() in ['will', 'shall']:
    #                 future_tense_verbs.append(next_word)
    #         elif current_pos in ['VBD', 'VBN']:
    #             past_tense_verbs.append(current_word)
        
    #     if future_tense_verbs:
    #         return 'future'
    #     elif past_tense_verbs:
    #         return 'past'
    #     else:
    #         return 'present'
    
    # def check_subject_verb_agreement(self):
    #     words = word_tokenize(self.preprocess(self.text))
    #     pos_tags = pos_tag(words)
    #     key_answer = self.data['key_answer'][1]

    #     subject_number = None
    #     verb_number = None
    #     is_compound_subject = False # Tandai buat melacak jika ada subject dan noun yang memiliki and
    #     modals = False # Tandai buat melacak jika ada verb modal

    #     subject = None
    #     verb = None

    #     for i, (word, tag) in enumerate(pos_tags):
    #         # cek untuk pronoun singular dan plural
    #         if tag == 'PRP':
    #             if tag in ['PRP', 'NN', 'NNP']:
    #                 subject = word
    #                 subject_number = 'singular'
    #             elif tag in ['NNS', 'NNPS']:
    #                 subject = word
    #                 subject_number = 'plural'
            
    #         # cek singular dan plural untuk noun
    #         elif tag in ['NN', 'NNP']:
    #             subject_number = 'singular'
    #         elif tag in ['NNS', 'NNPS']:
    #             subject_number = 'plural'

    #         if subject_number and i < len(pos_tags) - 2 and pos_tags[i + 1][0].lower() == 'and':
    #             next_tag = pos_tags[i + 2][1]
    #             if next_tag in ['PRP', 'NN', 'NNP', 'NNS', 'NNPS']:
    #                 is_compound_subject = True

    #         # cek kata kerja modal
    #         if tag == ['MD']:
    #             modals = True

    #         # menentukan singular dan plural untuk verb present tense
    #         if tag in ['VBZ']:
    #             verb = word
    #             verb_number = 'singular'
    #         elif tag in ['VBP', 'VB']:
    #             verb = word
    #             verb_number = 'plural'

    #         # menentukan singular dan plural di ver past tense
    #         elif tag in ['VBD', 'VBN']:
    #             if word.lower() == 'was':
    #                 verb_number = 'singular'
    #             elif word.lower() == 'were':
    #                 verb_number = 'plural'
    #             else:
    #                 #asumsi verb past tense lain, jadikan sama dengan subject
    #                 verb_number = subject_number

    #         # cek untuk agreement
    #         agreement = None
    #         if subject_number is not None and verb_number is not None:
    #             if is_compound_subject:
    #                 agreement = verb_number == 'plural'  # gabungan subject singular menjadi plural
    #             elif modals and tag == 'VB':  # setelah modal selalu verb untuk present tens
    #                 agreement = True
    #             else:
    #                 agreement = subject_number == verb_number

    #         if not agreement:
    #             for word, tag in pos_tags:
    #                 if tag in ['NN', 'NNS', 'NNP', 'NNPS', 'PRP']:
    #                     if subject is None:
    #                         subject = word
    #                 if tag in ['VB', 'VBP', 'VBZ', 'VBD', 'VBN', 'MD']:
    #                     if verb is None:
    #                         verb = word

    #         if subject and key_answer.lower() == subject.lower():
    #             return True  # key answer dan subject matching
    #         if verb and key_answer.lower() == verb.lower():
    #             return True  # key answer dan verb matching

    #     return agreement
        
    # def word_frequency(self, word, dictionary, freq_dict):
    #     i = 0
    #     stat = 0

    #     for lemma in dictionary:
    #         if word == lemma:
    #             stat = 1
    #             return freq_dict[i]
    #             break
    #         i += 1
    #     if stat == 0:
    #         return 0
        
    # def difficult_vocab(self):
    #     path = os.getcwd()
    #     data_path = path + '/data/lemmas_60k_words.xlsx'
    #     df = pd.read_excel(data_path, sheet_name='wordfrequency', usecols=['word', 'freq']).astype(str)
    #     dictionary = df.word.to_list()
    #     freq_dict = [int(item) for item in df.freq.to_list()]

    #     difficult_words = []
    #     for word in word_tokenize(self.preprocess(self.text)):
    #         freq = self.word_frequency(word, dictionary, freq_dict)
    #         if freq != 0:
    #             difficult_words.append({'word': word, 'frequency': self.normalize(freq, 100, max(freq_dict))})
        
    #     return self.sort_difficult_vocab(difficult_words)

    # def sort_difficult_vocab(self, difficult_words):
    #     sorted_list = sorted(difficult_words, key=lambda x: int(x["frequency"]), reverse=False)
    #     sum_freq = 0
    #     for word_freq in sorted_list:
    #         sum_freq += word_freq['frequency']
    #     sum_freq = format(sum_freq/len(sorted_list), '.3f')
    #     return float(sum_freq)

    # def normalize(self, value, min_value, max_value):
    #     return (value - min_value) / (max_value - min_value)
    
    # def error_type(self):
    #     verbs = ['VBG', 'VBN', 'VBD', 'VBZ', 'VBP', 'VB']
    #     pos = pos_tag(word_tokenize(self.preprocess(self.text)))
    #     key_answer_pos = pos[self.data['key_answer'][2]]
    #     if key_answer_pos[1] == 'IN':
    #         error_type = 'preprosition usage'
    #     elif key_answer_pos[1] == 'PRP$' or key_answer_pos[1] == 'PRP':
    #         error_type = 'pronoun usage'
    #     elif key_answer_pos[1] in verbs:
    #         error_type = 'tenses types'
    #     elif key_answer_pos[1] == 'CC':
    #         error_type = 'coherence'
    #     elif key_answer_pos[1] == 'DT':
    #         error_type = 'determiner'
    #     elif key_answer_pos[1].startswith("W"):
    #         error_type = '5w + 1h'
    #     else:
    #         error_type = 'other'
    #     return error_type
    
    # def error_type(self):
    #     pos = pos_tag(word_tokenize(self.preprocess(self.text)))
    #     key_answer_pos = pos[self.data['key_answer'][2]]
    #     if key_answer_pos[1] == 'IN':
    #         error_type = 'preprosition usage'
    #     elif key_answer_pos[1] == 'PRP$' or key_answer_pos[1] == 'PRP':
    #         error_type = 'pronoun usage'
    #     elif key_answer_pos[1] == 'VBG':
    #         error_type = 'present participle'
    #     elif key_answer_pos[1] == 'VBN':
    #         error_type = 'past participle'
    #     elif key_answer_pos[1] == 'VBD':
    #         error_type = 'past tense'
    #     elif key_answer_pos[1] == 'VBZ' or key_answer_pos[1] == 'VBP':
    #         error_type = '3rd person singular present'
    #     elif key_answer_pos[1] == 'CC':
    #         error_type = 'coherence'
    #     elif key_answer_pos[1] == 'DT':
    #         error_type = 'determiner'
    #     elif key_answer_pos[1].startswith("W"):
    #         error_type = '5w + 1h'
    #     else:
    #         print(key_answer_pos)
    #         error_type = 'other'
    #     return error_type
    



    # def get_key_index(self):
    #     options = ['A', 'B', 'C', 'D']
    #     for i in range(len(options)):
    #         if self.data['key_answer'][0] == options[i]:
    #             self.data['key_answer'].append(self.underline[i])
    