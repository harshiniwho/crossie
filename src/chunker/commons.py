import re
import nltk
import json

nltk.download('wordnet')

from nltk.corpus import wordnet

WORDS = wordnet.words()


def read_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def clean_list(data_list):
    clean_list = []
    for l in data_list:
        if isinstance(l, set):
            clean_list.append(list(l))
        else:
            clean_list.append(l)
    return clean_list


def find_definitions(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())    
    return set(synonyms)


def splitter(word):
    for i in range(1, len(word)):
        start = word[0:i]
        end = word[i:]
        yield (start, end)
        for split in splitter(end):
            result = [start]
            result.extend(split)
            yield result


def read_list_file(filename):
    list_data = []
    with open(filename, 'r') as f:
        for line in f:
            list_data.append(line.strip())
    return list_data


def check_valid_word(word):
    return word in WORDS
