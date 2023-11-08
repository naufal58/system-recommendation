import nltk
from nltk import word_tokenize, pos_tag, sent_tokenize
from nltk.corpus import cmudict
import pandas as pd
import os

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')

def preprocess(text):
    return text.replace('.', '').replace(',', '').lower()

def tag_features(text, underlined_index):
    pos = pos_tag(word_tokenize(preprocess(text)))
    underlined_postags = []
    irregular_verbs = []
    regular_verbs = []

    for i in range(len(pos)):
        if i in underlined_index:
            underlined_postags.append(pos[i])
        if pos[i][1] == 'VBN': ## Irregular verbs 
            irregular_verbs.append(pos[i])
        elif pos[i][1] == 'VBD': ## Regular verbs 
            regular_verbs.append(pos[i])

    return underlined_postags, len(irregular_verbs), len(regular_verbs)

def check_homophones(word):
    pronouncing_dict = cmudict.dict()
    entries = cmudict.entries()
    list_of_homophones = []
    for i in entries:
        if pronouncing_dict[word][0] == i[1] and len(list_of_homophones) <= 1:
            list_of_homophones.append(i)
        
    if len(list_of_homophones) > 1:
        return True, list_of_homophones
    return False, []

def count_homophones(text):
    num_of_homophones = 0
    for word in word_tokenize(preprocess(text)):
        try:
            homophones = check_homophones(word)
        except:
            continue
        if homophones[0] == True:
            num_of_homophones += 1
    return num_of_homophones

def syllable_count(word):
    d = cmudict.dict()
    # Check if the word is in the dictionary
    if word.lower() in d:
        # Use the first pronunciation and count the syllables
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]])
    else:
        # If the word is not in the dictionary, return a default value
        return 1

def flesch_reading_ease(text):
    words = word_tokenize(preprocess(text))
    sentences = sent_tokenize(text)

    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(syllable_count(word) for word in words)

    score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

    return score

def num_of_conjunctions(text):
    words = word_tokenize(preprocess(text))
    pos_tags = pos_tag(words)

    conjunctions = [word for word, pos_tag in pos_tags if pos_tag == 'CC']
    return len(conjunctions)

def tenses_type(text):
    words = word_tokenize(preprocess(text))
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

def word_frequency(word, dictionary, freq_dict):
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
    
def difficult_vocab(text):
    path = os.getcwd()
    data_path = path + '/data/lemmas_60k_words.xlsx'
    df = pd.read_excel(data_path, sheet_name='wordfrequency', usecols=['word', 'freq']).astype(str)
    dictionary = df.word.to_list()
    freq_dict = df.freq.to_list()

    difficult_words = []
    for word in word_tokenize(preprocess(text)):
        freq = word_frequency(word, dictionary, freq_dict)
        difficult_words.append({'word': word, 'frequency': freq})
    
    return sort_difficult_vocab(difficult_words)

def sort_difficult_vocab(difficult_words):
    sorted_list = sorted(difficult_words, key=lambda x: int(x["frequency"]), reverse=False)
    return sorted_list[:3]
