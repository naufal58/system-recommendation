import nltk
from nltk import word_tokenize, pos_tag, sent_tokenize
from nltk.corpus import cmudict
import pandas as pd

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')

def preprocess(text):
    return text.replace('.', '').lower()

def extractTagFeatures(text, underlinedIndex):
    pos = pos_tag(word_tokenize(text))
    underlinedPosTag = []
    irregularVerbs = []
    regularVerbs = []
    
    for i in range(len(pos)):
        if i in underlinedIndex:
            underlinedPosTag.append(pos[i])
        if pos[i][1] == 'VBN': ## Irregular verbs 
            irregularVerbs.append(pos[i])
        elif pos[i][1] == 'VBD': ## Regular verbs 
            regularVerbs.append(pos[i])
    return underlinedPosTag, irregularVerbs, regularVerbs

def checkHomophones(word):
    # Access the CMU Pronouncing Dictionary
    pronouncing_dict = cmudict.dict()
    entries = cmudict.entries()
    listOfHomophones = []
    for i in entries:
        if pronouncing_dict[word][0] == i[1]:
            listOfHomophones.append(i)
        
    if len(listOfHomophones) > 1:
        return True, listOfHomophones
    return False, []

def countHomophones(text):
    numOfHomophones = 0
    for word in word_tokenize(preprocess(text)):
        homophones = checkHomophones(word)
        if homophones[0] == True:
            numOfHomophones += 1
    return numOfHomophones

def syllableCount(word):
    d = cmudict.dict()
    # Check if the word is in the dictionary
    if word.lower() in d:
        # Use the first pronunciation and count the syllables
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]])
    else:
        # If the word is not in the dictionary, return a default value
        return 1

def fleschReadingEase(text):
    words = word_tokenize(preprocess(text))
    sentences = sent_tokenize(text)

    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(syllableCount(word) for word in words)

    score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

    return score

def numOfConjunctions(text):
    words = word_tokenize(preprocess(text))
    pos_tags = pos_tag(words)

    conjunctions = [word for word, pos_tag in pos_tags if pos_tag == 'CC']
    return len(conjunctions)

def tensesType(text):
    words = word_tokenize(preprocess(text))
    pos_tags = pos_tag(words)

    future_tense_verbs = []
    present_tense_verbs = []
    past_tense_verbs = []

    for i in range(len(pos_tags)-1):
        current_word, current_pos = pos_tags[i]
        next_word, next_pos = pos_tags[i+1]

        if current_pos == 'MD' and next_pos == 'VB':
            # Check for modal verb 'will' or 'shall' followed by a base form verb
            if current_word.lower() in ['will', 'shall']:
                future_tense_verbs.append(next_word)
        # elif current_pos in ['VB', 'VBG', 'VBP', 'VBZ']:
        #     present_tense_verbs.append(current_word)
        elif current_pos in ['VBD', 'VBN']:
            past_tense_verbs.append(current_word)
    
    if future_tense_verbs:
        return 'future'
    elif past_tense_verbs:
        return 'past'
    else:
        'present'