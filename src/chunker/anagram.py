import sys
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

WORDS = set()
for word in WORDS_ALL:
    WORDS.add(word)

def break_word(word):
    length = len(word) + 1
    return [word[x:y] for x, y in combinations(range(length), r=2)]


def generate_all_anagrams(word):
    return ["".join(perm) for perm in itertools.permutations(word)]


def prerequisites():
    anagram_indicators = commons.read_list_file(DATA_DIR + ABBREVIATIONS_FILE)
    linking_words = commons.read_list_file(DATA_DIR + LINKING_WORDS_FILE)
    return linking_words, anagram_indicators


def check_valid_anagrams(anagrams):
    all_words = set()
    valid_words = set()
    for anagram in anagrams:
        words = break_word(anagram)
        all_words.update(words)
    for word in all_words:
        if word in WORDS:
            if len(word) == 1:
                if word in ONE_LETTER_WORDS:
                    valid_words.add(word)
            else:
                valid_words.add(word)
    return valid_words


def check_valid_splits(all_anagrams, valid_words):
    valid_splits = []
    for word in all_anagrams:
        words = break_word(word)  
        splits = list(commons.splitter(word))
        for split in splits:
            valid = True
            for sp in split:
                if not (sp in valid_words):
                    valid = False
                    break
            if valid:
                valid_splits.append(split)
    return valid_splits


def write_file(word, possibilities):
    with open(f"{word}-anagram-possibilities", 'w') as f:
        for split in possibilities:
            out = ""
            for word in split:
                out += f"{word}+"
            out = out[:-1] + "\n"
            f.write(out)


@click.command()
@click.option("--word", "-w", help="Word to generate anagrams for", required=True)
def main(word):
    linking_words, anagram_indicators = prerequisites()
    all_anagrams = generate_all_anagrams(word)
    valid_words = check_valid_anagrams(all_anagrams)
    valid_splits = check_valid_splits(all_anagrams, valid_words)
    write_file(word, valid_splits)


if __name__ == "__main__":
    main()
