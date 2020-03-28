import os
import string
import time
import json
from nltk.stem.snowball import SnowballStemmer
from itertools import chain
from tqdm import tqdm
import pdb


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
        cache_file = os.path.join(self.dirname, 'index_cache.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self.metadata, self.posting = json.load(f)
            print('Index of {} corpus loaded from {}'.format(os.path.dirname(self.dirname), cache_file))
            return
        print('Creating index for {} corpus...'.format(os.path.dirname(self.dirname)))
        start_time = time.time()
        files = self.get_files(self.dirname)
        file_token_list = list(list())  # containing token list for each file
        for file in tqdm(files[:10]):
            with open(file) as f:
                file = os.path.splitext(os.path.basename(file))[0]
                file_token_list.append(self.linguistic(self.tokenization(f.read(), file)))
        # pdb.set_trace()
        all_token_list = list(chain.from_iterable(file_token_list))  # containing tokens from all documents
        print('Start sorting the tokens from all documents.')
        sort_start = time.time()
        self.sorting(all_token_list)  # in-place sorting, save memory
        print('Sorting finished in {:.2f} s.'.format(time.time()-sort_start))
        for token in all_token_list:
            self.add(token)
        total_time = time.time() - start_time
        print('Index created in {:d} min {:.2f} s.'.format(int(total_time / 60), total_time % 60))
        print("Saving index and metadata to {}".format(cache_file))
        with open(cache_file, "w") as f:
            f.write(json.dumps([self.metadata, self.posting]))
            f.flush()

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
        posting_lists = [self.posting[token] if token in self.posting else [] for token in tokens]
        result = self.merge(posting_lists)
        novels = [Novel(os.path.join(self.dirname, doc_id+'.txt'), self.metadata[doc_id]) for doc_id in result]
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
        tokens_modified = list(set(tokens_modified))  # delete those repeat pairs
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
        # collapse identical tokens together
        if token in self.posting:
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
