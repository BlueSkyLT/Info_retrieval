import os
import string
import time
import pickle
from nltk.stem.snowball import SnowballStemmer
from itertools import chain
from tqdm import tqdm


# def get_files(dirname: str):
#     """
#     Args:
#         dirname (str): path to directory
#     Returns:
#         file_list (list): full paths to files in the directory
#     """
#     file_list = list()
#     for filename in os.listdir(dirname):
#         file_list.append(os.path.join(dirname, filename))
#     return file_list
#
#
# def tokenization(content: str, doc_id: str):
#     """
#     Args:
#         content (str): Document text
#         doc_id(str): Document Id
#     Returns:
#         tokens (list): Token-docId pairs
#     """
#     tokens = list()
#     lines = content.splitlines()
#     for line in lines:
#         token = line.split()  # default split by whitespace
#         tokens.extend(zip(token, len(token) * [doc_id]))
#     return tokens
#
#
# def linguistic(tokens: list):
#     """
#     Remove punctuation symbols, lowercasing and stemming.
#     Args:
#         tokens (list): Original token-docId pairs
#     Returns:
#         tokens_modified (list): Modified token-docId pairs
#     """
#     tokens_modified = list()
#     stemmer = SnowballStemmer("english")
#     translator = str.maketrans('', '', string.punctuation)
#     for pairs in tokens:
#         token = pairs[0].translate(translator).lower()  # remove punctuation symbols, lowercasing
#         if token:  # filter out those empty token
#             tokens_modified.append((stemmer.stem(token), pairs[1]))  # stemming
#     return tokens_modified
#
#
# def sorting(tokens: list):
#     """
#     Perform sorting of the token list, first by tokens (alphabetical order),
#     and then by document ids (alphabetical order).
#     Args:
#         tokens (list): token list to be sorted
#     Returns:
#         tokens_sorted (list): sorted token list
#     """
#     tokens.sort(key=lambda x: (x[0], x[1]))
#
#
# class Posting(object):
#     """
#     Create inverted index from sorted list of of token-docId pairs.
#     """
#     def __init__(self):
#         self.posting = dict()
#
#     def add(self, token):
#         if token[0] in self.posting:
#             if token[1] not in self.posting[token[0]][1]:  # collapse identical tokens together
#                 self.posting[token[0]][1].append(token[1])
#                 self.posting[token[0]][0] += 1
#         else:
#             self.posting[token[0]] = [1, [token[1]]]


class Dataset(object):
    """
    Create index for a dataset.
    Args:
        dirname (str): path to the dataset directory
    """
    def __init__(self, dirname):
        self.dirname = dirname
        self.stemmer = SnowballStemmer("english")
        self.translator = str.maketrans('', '', string.punctuation)
        self.posting = dict()
        self.metadata = dict(dict())
        self.create_index()

    def create_index(self):
        cache_file = os.path.join(self.dirname, 'index_cache.pkl')
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                self.metadata, self.posting = pickle.load(f)
            print('Index of {} corpus loaded from {}'.format(os.path.dirname(self.dirname), cache_file))
            return
        print('Creating index for {} corpus...'.format(os.path.dirname(self.dirname)))
        start_time = time.time()
        files = self.get_files(self.dirname)
        file_token_list = list(list())  # containing token list for each file
        for file in tqdm(files[:10]):
            with open(file) as f:
                # print(file)
                file_token_list.append(self.linguistic(self.tokenization(f.read(), file)))
        all_token_list = list(chain.from_iterable(file_token_list))  # containing tokens from all documents
        self.sorting(all_token_list)  # in-place sorting, save memory
        for token in all_token_list:
            self.add(token)
        print('Done in {:.2f}s.'.format(time.time() - start_time))
        with open(cache_file, 'wb') as f:
            pickle.dump((self.metadata, self.posting), f, pickle.HIGHEST_PROTOCOL)

    def query(self, query: str):
        """
        Perform the same tokenization and lexical transformation on query, and get the search results.
        Args:
            query (str): input query
        Returns:
            Novels (list): a list that contains Novel Class objects.
        """
        tokens = query.split()
        tokens = [self.stemmer.stem(token.translate(self.translator).lower()) for token in tokens]
        posting_lists = [self.posting[i] if i in self.posting else [] for i in tokens]
        result = self.merge(posting_lists)
        novels = [Novel(doc_id, self.metadata[doc_id]) for doc_id in result]
        return novels

    @staticmethod
    def merge(posting_lists: list):
        """
        Merge postings lists.
        Args:
            posting_lists (list): a list that contains postings lists to be merged.
        Returns:
            posting_merged (list): merged postings list.
        """
        posting_lists.sort(key=lambda x: len(x))  # in order to start merging from the shortest posting list
        posting_set = set(posting_lists[0])
        for i in range(1, len(posting_lists)):
            posting_set &= set(posting_lists[i])
        posting_merged = list(posting_set)
        return posting_merged

    @staticmethod
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

    def tokenization(self, content: str, doc_id: str):
        """
        Tokenization and collect metadata
        Args:
            content (str): Document text
            doc_id(str): Document Id
        Returns:
            tokens (list): Token-docId pairs
        """
        self.metadata[doc_id] = dict()
        tokens = list()
        lines = content.splitlines()
        keys = ['Title', 'Author', 'Release Date', 'Language', 'Character set encoding']
        for i, line in enumerate(lines):
            if i < 30:
                for j in range(len(keys)):
                    if keys[j] in line:
                        self.metadata[doc_id][keys[j]] = line.strip().replace(keys[j]+': ', '')
            token = line.split()  # default split by whitespace
            tokens.extend(zip(token, len(token) * [doc_id]))
        return tokens

    def linguistic(self, tokens: list):
        """
        Remove punctuation symbols, lowercasing and stemming.
        Args:
            tokens (list): Original token-docId pairs
        Returns:
            tokens_modified (list): Modified token-docId pairs
        """
        tokens_modified = list()

        for pairs in tokens:
            token = pairs[0].translate(self.translator).lower()  # remove punctuation symbols, lowercasing
            if token:  # filter out those empty token
                tokens_modified.append((self.stemmer.stem(token), pairs[1]))  # stemming
        return tokens_modified

    @staticmethod
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

    def add(self, token_docid):
        """
        Transform and add token-docId pairs into postings.
        Args:
            token_docid (tuple): token-docId pairs to be added
        """
        token = token_docid[0]
        doc_id = token_docid[1]
        if token in self.posting:
            if doc_id not in self.posting[token]:  # collapse identical tokens together
                self.posting[token].append(doc_id)
        else:
            self.posting[token] = [doc_id]


class Novel(object):
    """
    Args:
        docid (str): docId of the novel
        metadata (dict): Title, Author, Release Date, Language, Character set encoding
    """
    def __init__(self, docid, metadata):
        self.docid = docid
        self.title = metadata.get('Title')
        self.author = metadata.get('Author')
        self.release_date = metadata.get('Release Date')
        self.language = metadata.get('Language')
        self.encoding = metadata.get('Character set encoding')

    def print(self):
        print('DocId: {}'.format(self.docid))
        print('Title: {}'.format(self.title))
        print('Author: {}'.format(self.author))
        print('Release Date: {}'.format(self.release_date))
        print('Language: {}'.format(self.language))
        print('Character set encoding: {}'.format(self.encoding))
