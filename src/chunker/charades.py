import sys
from itertools import combinations

import click
from nltk.corpus import wordnet

from config import *
import commons


def break_word(word):
    length = len(word) + 1
    return [word[x:y] for x, y in combinations(range(length), r=2)]


def prerequisites():
    charade_indicators = commons.read_list_file(DATA_DIR + CHARADES_FILE)
    linking_words = commons.read_list_file(DATA_DIR + LINKING_WORDS_FILE)
    abbreviations = commons.read_json_file(DATA_DIR + ABBREVIATIONS_FILE)
    return linking_words, charade_indicators, abbreviations


def check_valid_splits(word, abbreviations):
    words = break_word(word)
    valid_words = []
    for w in words:
        if commons.check_valid_word(w):
            valid_words.append(w)    
    splits = list(commons.splitter(word))
    splits = commons.clean_list(splits)
    valid_splits = []
    for split in splits:
        valid = True
        for sp in split:
            if not ((sp in abbreviations) or (sp in valid_words)):
                valid = False
                break
        if valid and len(split) <= MAX_SPLIT_SIZE:
            valid_splits.append(split)
    return valid_splits, valid_words


def generate_charades(valid_splits, abbreviations, valid_words):
    possibilities = []
    for split in valid_splits:
        word = []
        for sp in split:
            letter = []
            if sp in abbreviations:
                if isinstance(abbreviations[sp], list):
                    letter.extend(abbreviations[sp])
                else:
                    letter.append(abbreviations[sp])
            if sp in valid_words:
                letter.extend(commons.find_definitions(sp))
            word.append(letter)
        possibilities.append(word)
    return possibilities


def write_file(word, possibilities):
    with open(f"{word}-charades-possibilities", 'w') as f:
        for word in possibilities:
            out = ""
            if (len(word) == 2):
                for letter in word[0]:
                    for second_letter in word[1]:
                        out += f"{letter}+{second_letter}\n"
            elif (len(word) == 3):
                for letter in word[0]:
                    for second_letter in word[1]:
                        for third_letter in word[2]:
                            out += f"{letter}+{second_letter}+{third_letter}\n"
            elif (len(word) == 1):
                for letter in word:
                    out += f"{letter}\n"
            else:
                continue
            out = out[:-1]
            f.write(out)


@click.command()
@click.option("--word", "-w", help="Word to generate charades for", required=True)
def main(word):
    linking_words, charade_indicators, abbreviations = prerequisites()
    valid_splits, valid_words = check_valid_splits(word, abbreviations)
    charade_possibilities = generate_charades(valid_splits, abbreviations, valid_words)
    write_file(word, charade_possibilities)


if __name__ == "__main__":
    main()
