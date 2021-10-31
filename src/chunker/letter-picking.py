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

WORDS_ALL = wordnet.words()
splits = []

WORDS = set()
for word in WORDS_ALL:
    WORDS.add(word)


def split_word(word):
    return list(word)


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
    return matched_words


def generate_all_letter_picking(letter_list):
    first_letter_picking = []
    last_lettter_picking = []
    matches = {}
    for letter in letter_list:
        regex = re.escape(letter) + r'[a-zA-Z]*'
        matched = find_valid_regex_word(regex)
        first_letter_picking.append(matched)
        regex = r'[a-zA-Z]*' + re.escape(letter) + r'$'
        matched = find_valid_regex_word(regex)
        last_lettter_picking.append(matched)
    return first_letter_picking, last_lettter_picking


def prerequisites():
    first_letter_indicators = commons.read_list_file(DATA_DIR + FIRST_PICKING_FILE)
    last_letter_indicators = commons.read_list_file(DATA_DIR + LAST_PICKING_FILE)
    alternate_letter_indicators = commons.read_list_file(DATA_DIR + ALTERNATE_PICKING_FILE)
    linking_words = commons.read_list_file(DATA_DIR + LINKING_WORDS_FILE)
    return linking_words, first_letter_indicators, last_letter_indicators, alternate_letter_indicators


def write_file(word, possibilities, file_type):
    with open(f"{word}-{file_type}-possibilities", 'w') as f:
        json.dump(possibilities, f)


@click.command()
@click.option("--word", "-w", help="Word to generate letter-picking for", required=True)
def main(word):
    linking_words, first_letter_indicators, last_letter_indicators, alternate_letter_indicators = prerequisites()
    letter_list = split_word(word)
    first_letters, last_letters = generate_all_letter_picking(letter_list)
    write_file(word, first_letters, 'first')
    write_file(word, last_letters, 'last')


if __name__ == "__main__":
    main()
