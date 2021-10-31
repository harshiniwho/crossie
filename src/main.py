import re
import nltk
import json
from itertools import combinations

nltk.download('wordnet')

from nltk.corpus import wordnet


def find_definitions(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())    
    return set(synonyms)


def break_word(word):
    length = len(word) + 1
    return [word[x:y] for x, y in combinations(range(length), r=2)]


def splitter(word):
    for i in range(1, len(word)):
        start = word[0:i]
        end = word[i:]
        yield (start, end)
        for split in splitter(end):
            result = [start]
            result.extend(split)
            yield result


def find_anagrams(word):
    if len(word) <= 1:
        return word
    else:
        tmp = []
        for perm in find_anagrams(word[1:]):
            for i in range(len(word)):
                tmp_word = perm[:i] + word[0:1] + perm[i:]
                if tmp_word in wordnet.words():
                    tmp.append(tmp_word)
        return tmp


def construct_telescopic_re(word):
    characters = list(word)


def construct_first_of_re(word):
    characters = list(word)
    constraints = []
    for c in characters:
        constraints.append(re.escape(c) + r'[a-z]')
    return constraints


def construct_last_of_re(word):
    characters = list(word)
    constraints = []
    for c in characters:
        constraints.append(r'[a-z]' + re.escape(c))
    return constraints


def construct_every_other_re(word):
    characters = list(word)
    constraints = []
    for c in characters:
        constraints.append(r'[a-z]' + re.escape(c))
    return constraints    


def construct_enum(word):
    return "(" + str(len(word)) + ")"


def write_to_file(word, data):
    with open(word + '-possibilities.csv', 'w') as f:
        json.dump(data, f)


def write_list_to_file(filename, list_data):
    with open("data/" + filename, 'w') as f:
        for d in list_data:
            f.write(d + "\n")


def main():
    print("Enter word to build clue for")
    word = input()
    data = {}
    # construct_first_of_re(word)
    # data["word"] = word
    data["definitions"] = find_definitions(word)
    write_list_to_file(word, data["definitions"])
    # data["enum"] = construct_enum(word)
    # data["splits"] = list(splitter(word))
    # data["first-letter"] = construct_first_of_re(word)
    # data["last-letter"] = construct_last_of_re(word)
    # write_to_file(word, data)


if __name__ == "__main__":
    main()
