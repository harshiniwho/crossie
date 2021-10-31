import sys
import re
import json
import itertools
from itertools import combinations

import click
import nltk
from nltk.corpus import wordnet

from config import *
import commons

nltk.download('wordnet')

from nltk.corpus import wordnet

WORDS_ALL = wordnet.words()
splits = []

WORDS = set()
for word in WORDS_ALL:
    WORDS.add(word)


def check_valid_words(splits):
    valid_words = set()
    for split in splits:
        for sp in split:
            if len(sp) == 1:
                if sp in ONE_LETTER_WORDS:
                    valid_words.add(sp)
            elif sp in WORDS:
                valid_words.add(sp)
    return valid_words


def generate_splits(word):
    splits = list(commons.splitter(word))
    final_splits = []
    valid_words = check_valid_words(splits)
    for split in splits:
        if len(split) <= 3:
            if len(split) == 3:
                if split[2] in valid_words:
                    final_splits.append(split)
            else:
                final_splits.append(split)
    final_splits.append([word])
    return final_splits, valid_words


def find_valid_regex_word(regex):
    matched_words = []
    try:
        for word in WORDS:
            if re.match(regex, word):
                matched_words.append(word)
    except:
        print("failed regex " + regex)
        exit(1)
    return matched_words


def generate_all_telescopes(splits):
    telescopes = []
    matches = {}
    for split in splits:
        telescope = {}
        if len(split) == 3:
            start = re.escape(split[0]) + r'[a-zA-Z]*' 
            end = r'[a-zA-Z]*' + re.escape(split[2]) + r'$'
            start_words = find_valid_regex_word(start)
            end_words = find_valid_regex_word(end)
            telescope["start"] = start_words
            telescope["mid"] = split[1]
            telescope["end"] = end_words
        elif len(split) == 2:
            start = re.escape(split[0]) + r'[a-zA-Z]*' 
            end = r'[a-zA-Z]*' + re.escape(split[1])  + r'$'
            start_words = find_valid_regex_word(split[0])
            end_words = find_valid_regex_word(split[1])
            telescope["start"] = start_words
            telescope["end"] = end_words
        else:
            match_exp = r'[a-zA-Z]*' + re.escape(split[0]) + r'[a-zA-Z]*'
            matched_words = find_valid_regex_word(match_exp)
            telescope["one_word"] = matched_words
        telescopes.append(telescope)
    return telescopes


def prerequisites():
    telescopic_indicators = commons.read_list_file(DATA_DIR + CONTAINERS_FILE)
    linking_words = commons.read_list_file(DATA_DIR + LINKING_WORDS_FILE)
    return linking_words, telescopic_indicators


def write_file(word, possibilities):
    with open(f"{word}-telescope-possibilities", 'w') as f:
        json.dump(possibilities, f)


@click.command()
@click.option("--word", "-w", help="Word to generate telescopic for", required=True)
def main(word):
    linking_words, telescopic_indicators = prerequisites()
    valid_splits, valid_words = generate_splits(word)
    telescopes = generate_all_telescopes(valid_splits)
    write_file(word, telescopes)


if __name__ == "__main__":
    main()
