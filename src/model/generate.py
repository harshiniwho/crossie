import click

from config import *
from model import *


def fetch_file_chunks(filename):
    filename_cut = filename[filename.find('-')+1:]
    word = filename[:filename.find('-')]
    enum = '(' + str(len(word)) + ')'
    clue_type = filename_cut[:filename_cut.find('-')]
    return word, enum, clue_type


def reconstruct_clue_chunks(filename):
    clue_chunks = []
    with open(filename) as f:
        for line in f:
            line = line.replace('\n', '')
            clue_chunks.append(line)
    return clue_chunks


def clean_poss(word):
  return word.replace('+', ' ').replace('_', ' ').replace('(', '').replace(')', '')


def read_list_file(filename):
    list_data = set()
    with open(filename, 'r') as f:
        for line in f:
            list_data.add(line.strip())
    return list_data


def create_clue_dictionary(word, clue_type):
    definitions = read_list_file(DATA_DIR + word)
    linking_words = read_list_file(DATA_DIR + 'linking-words')
    indicators = read_list_file(DATA_DIR + clue_type)
    return definitions, linking_words, indicators


def generate_brute_force(clue_chunks, definitions, linking_words):
    clues = []
    for chunk in clue_chunks:
        phrase = clean_poss(chunk)
        for linker in linking_words:
            for syn in definitions:
            # def at beginning
                clue = syn + ' ' + linker + ' ' + phrase
                clue.replace('_', ' ')
                clues.append(clue)
                # def at end
                clue = phrase + ' ' + linker + ' ' + syn
                clue.replace('_', ' ')
                clues.append(clue)
    return clues


def check_all_linking_preds(preds, linking_words):
    valid_links = []
    for pred in preds:
        if pred in linking_words:
            valid_links.append(pred)
    return valid_links


def construct_clue(phrase, definitions, linking_word, enum, clue_type):
    if clue_type == "end":
        for definition in definitions:
            return f"{phrase} {linking_word} {definition} {enum}"
    else:
        return f"{definitions} {linking_word} {phrase} {enum}"


def generate_def_end_with_splits(clue_chunks, definitions, linking_words, enum):
    next_poss = {}
    generated_clues = []
    phrases = []
    for poss in clue_chunks:
        poss = poss.replace('_', '+')
        splits = poss.split('+')
        if len(splits) > 3:
            continue
        word1 = splits[0]
        word2 = splits[1]
        if word1 not in next_poss:
            next = fetch_next_words(word1, 200)
            next_poss[word1] = next
        if word2 in next_poss[word1]:
            phrase = word1 + ' ' + word2
            if phrase not in next_poss:
                next = fetch_next_words(phrase, 200)
                next_poss[phrase] = next
            if len(splits) == 2:
                linking_word = check_all_linking_preds(next_poss[phrase], linking_words)
            if linking_word:
                for link in linking_word:
                    generated_clues.append(construct_clue(poss, definitions, link, enum, "end"))
                phrases.append(phrase)
            else:
                word3 = splits[2]
                if word3 in next_poss[phrase]:
                    phrase += ' ' + word3
                    if phrase not in next_poss:
                        next_poss[phrase] = fetch_next_words(phrase, 200)
                    linking_word = check_all_linking_preds(next_poss[phrase], linking_words)
                    if linking_word:
                        for link in linking_word:
                            generated_clues.append(construct_clue(poss, definitions, link, enum, "end"))
                        phrases.append(phrase)

    for poss in clue_chunks:
        poss = clean_poss(poss)
        next = fetch_next_words(poss, 200)
        linking_word = check_all_linking_preds(next, linking_words)
        if linking_word:
            for link in linking_word:
                generated_clues.append(construct_clue(poss, definitions, link, enum, "end"))
            phrases.append(poss)
    return generated_clues, phrases


def parse_output(text):
    valid_text = []
    for line in text:
        s = parser.parse(text)
        if 'errors' not in str(s):
            valid_clues.append(text)
    return valid_text


def check_phrases(word, phrases):
    split = phrases.split(' ')
    if word == split[0]:
        return True
    return False


def generate_def_beg_with_splits(definitions, linking_words, phrases, enum):
    generated_clues = []
    for definition in definitions:
        res = fetch_next_words(definition, 200)
        links = check_all_linking_preds(res, linking_words)
        for link in links:
            if link:
                phrase = definition + ' ' + link
                wordplays = fetch_next_words(phrase, 200)
                for wordplay in wordplays:
                    if check_phrases(wordplay, phrases):
                        generated_clues.append(construct_clue(phrase, definition, link, enum, "beg"))
    return generated_clues


def write_list_to_file(filename, list_data):
    with open(filename, 'w') as f:
        for d in list_data:
            f.write(d + "\n")


@click.command()
@click.option("--filename", "-f", help="Filename to generate clues for", required=True)
def main(filename):
    word, enum, clue_type = fetch_file_chunks(filename)
    clue_chunks = reconstruct_clue_chunks(filename)
    definitions, linking_words, indicators = create_clue_dictionary(word, clue_type)

    brute_force_clues = generate_brute_force(clue_chunks, definitions, linking_words)

    generated_clues, phrases = generate_def_end_with_splits(clue_chunks, definitions, linking_words, enum)
    generated_clues.extend(generate_def_beg_with_splits(phrases, definitions, linking_words, enum))

    write_list_to_file(f'brute-force-clues-{word}', brute_force_clues)
    write_list_to_file(f'generated-clues-{word}', generated_clues)


if __name__ == "__main__":
    main()
