import marisa_trie
import nltk
nltk.download('words')

from nltk.corpus import words


def find_definitions(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())    
    return set(synonyms)


def create_word_list():
    word_list = words.words()
    with open('words.txt', 'w') as f:
        for word in word_list:
            f.write(word + "\n")


def clean_abbreviation_file():
    with open('data/abbreviations', 'w') as out:
        with open('data/temp-abbreviations', 'r') as inp:
            for line in inp:
                line = line.replace('\n', '')
                out.write(line + ",\n")


def load_trie(filename):
    with open(filename) as dict_trie:
        trie = marisa_trie.Trie()
        trie.read(dict_trie)
        return trie


def load_text_file(filename):
    with open(filename) as text_file:
        words = [word.strip() for word in text_file]
        trie = marisa_trie.Trie(words)
        return trie


def load_dictionary(filename):
    extension = filename.split('.')[-1]
    if extension == 'marisa':
        return load_trie(filename)
    elif extension == 'txt':
        return load_text_file(filename)
