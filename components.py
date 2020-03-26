import os
import string
from nltk.stem.snowball import SnowballStemmer


def get_files(dirname: str):
    """
    Args:
        dirname (str): path to directory
    Returns:
        file_list (list): full paths to files in the directory
    """
    file_list = list()
    for filename in os.listdir(dirname):
        file_list.append(os.path.join(dirname, filename))
    return file_list


def tokenization(content: str, doc_id: str):
    """
    Args:
        content (str): Document text
        doc_id(str): Document id
    Returns:
        tokens (list): Token-document id pairs
    """
    tokens = list()
    lines = content.splitlines()
    for line in lines:
        token = line.split()  # default split by whitespace
        tokens.extend(zip(token, len(token) * [doc_id]))
    return tokens


def linguistic(tokens: list):
    """
    Remove punctuation symbols, lowercasing and stemming.
    Args:
        tokens (list): Original token-document id pairs
    Returns:
        tokens_modified (list): Modified token-document id pairs
    """
    tokens_modified = list()
    stemmer = SnowballStemmer("english")
    translator = str.maketrans('', '', string.punctuation)
    for pairs in tokens:
        token = pairs[0].translate(translator).lower()  # remove punctuation symbols, lowercasing
        if token:  # filter out those empty token
            tokens_modified.append((stemmer.stem(token), pairs[1]))  # stemming
    return tokens_modified


def sorting(tokens: list):
    """
    Perform sorting of the token list, first by tokens (alphabetical order),
    and then by document ids (alphabetical order).
    Args:
        tokens (list): token list to be sorted
    Returns:
        tokens_sorted (list): sorted token list
    """
    tokens.sort(key=lambda x: (x[0], x[1]))


class Posting(object):
    """
    Perform sorting of the token list, first by tokens (alphabetical order),
    and then by document ids (alphabetical order).
    """
    def __init__(self):
        self.posting = dict()

    def add(self, token):
        if token[0] in self.posting:
            if token[1] not in self.posting[token[0]][1]:  # collapse identical tokens together
                self.posting[token[0]][1].append(token[1])
                self.posting[token[0]][0] += 1
        else:
            self.posting[token[0]] = [1, [token[1]]]

    # def sort(self):
    #     self.posting = sorted(self.posting, key=lambda x: -x[1][0])
