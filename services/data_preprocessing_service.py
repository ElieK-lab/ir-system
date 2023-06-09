import re

import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
import spacy
import datefinder
import json
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
from autocorrect import Speller

stop_words = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
spell = Speller(lang='en')

with open('C:\\Users\\Elie\\Desktop\\testpython\\abbreviations.json') as json_file:
    abbreviations = json.load(json_file)


######################################################################
def remove_punctuation_marks(sentence):
    return re.sub(r'[^_\w\s]', '', sentence)


def remove_unalpah_chars(sentence):
    return re.compile('[^a-zA-Z0-9_\s]').sub('', sentence)


def lemmatize_text(text):
    result = []
    for word in word_tokenize(text):
        doc = nlp(word)
        lemmas = [token.lemma_ for token in doc if not token.is_stop]
        if len(lemmas) > 0:
            result.append(lemmas[0])
    return ' '.join(result)


def spell_correction(text):
    return spell(text)


def replace_abbreviations(text):
    result = []
    for token in text.split():
        if token in abbreviations.keys():
            result.append(abbreviations.get(token))
        else:
            result.append(token)
    return ' '.join(result)


def convert_dates(text):
    text = text.replace('_', ' ')
    matches = datefinder.find_dates(text, source=True, strict=True)
    for match in matches:
        converted_token = match[0].strftime("%Y_%m_%d")
        text = text.replace(match[1], converted_token)
    return text


######################################################################


def apply_preprocessing_text(text):
    text = str(text)
    with open('C:\\Users\\Elie\\Desktop\\testpython\\data_set_name.json') as json_file:
        dataset_name = json.load(json_file)['name']
    if dataset_name == 'qoura':
        cleanSentence = convert_dates(str(text))
        cleanSentence = replace_abbreviations(cleanSentence)
        cleanSentence = str(cleanSentence).lower()
        cleanSentence = lemmatize_text(cleanSentence)
        cleanSentence = remove_punctuation_marks(cleanSentence)
        cleanSentence = remove_unalpah_chars(cleanSentence)
        cleanSentence = spell_correction(cleanSentence)
        print(f"Qoura query after preprocessing :{cleanSentence}")
        return cleanSentence
    elif dataset_name == 'antique':
        text = text.lower()
        text = ' '.join([str(word).translate(translation_table) for word in word_tokenize(text)])
        text = ' '.join([word for word in word_tokenize(text) if word not in stop_words])
        print(f"Antique query after preprocessing :{text}")
        return str(text)


translation_table = {
    48: " zero ",  # 0
    49: " one ",  # 1
    50: " two ",  # 2
    51: " three ",  # 3
    52: " four ",  # 4
    53: " five ",  # 5
    54: " six ",  # 6
    55: " seven ",  # 7
    56: " eight ",  # 8
    57: " nine ",  # 9
    33: ' ',  # !
    34: ' ',  # "
    35: ' ',  # #
    36: ' ',  # $
    37: ' ',  # %
    38: ' ',  # &
    39: ' ',  # '
    40: ' ',  # (
    41: ' ',  # )
    42: ' ',  # *
    43: ' ',  # +
    44: ' ',  # ,
    45: ' ',  # -
    46: ' ',  # .
    47: ' ',  # /
    58: ' ',  # :
    59: ' ',  # ;
    60: ' ',  # <
    61: ' ',  # =
    62: ' ',  # >
    63: ' ',  # ?
    64: ' ',  # @
    91: ' ',  # [
    92: ' ',  # \
    93: ' ',  # ]
    94: ' ',  # ^
    95: ' ',  # _
    96: ' ',  # `
    123: ' ',  # {
    124: ' ',  # |
    125: ' ',  # }
    126: ' ',  # ~
}
