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

    def query(self, query: str, func: str):
        """
        Perform the same tokenization and lexical transformation on query, and get the search results.
        Args:
            query (str): input query
            func (str): specify the merge method
        Returns:
            novels (list): a list that contains Novel Class objects.
        """
        tokens = query.split()
        tokens = [self.stemmer.stem(token.translate(self.translator).lower()) for token in tokens]
        posting_lists = [self.posting[i] if i in self.posting else [] for i in tokens]

        function_name = 'self.' + func
        result = eval(function_name)(posting_lists)
        novels = [Novel(doc_id, self.metadata[doc_id]) for doc_id in result]
        return novels

    @staticmethod
    def merge_py(posting_lists: list):
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
    def merge_baseline(posting_lists: list):
        """
        Merge postings lists.
        Args:
            posting_lists (list): a list that contains postings lists to be merged.
        Returns:
            posting_merged (list): merged postings list.
        """
        posting_merged = list()
        for list_i in range(len(posting_lists) - 1):
            list_j = list_i + 1

            posting_lists_i = posting_lists[list_i]
            posting_lists_j = posting_lists[list_j]

            for element_i in range(len(posting_lists_i)):
                for element_j in range(len(posting_lists_j)):
                    if posting_lists_i[element_i] == posting_lists_j[element_j]:
                        posting_merged.append(posting_lists_i[element_i])
                        break
        if len(posting_lists) == 1:
            posting_merged = posting_lists[0]

        return posting_merged

    @staticmethod
    def merge_linear(posting_lists: list):
        """
        Merge postings lists.
        Args:
            posting_lists (list): a list that contains postings lists to be merged.
        Returns:
            posting_merged (list): merged postings list.
        """
        posting_merged = list()
        name = locals()
        for index_list in range(len(posting_lists)):
            name['list'+str(index_list)] = posting_lists[index_list]
            name['list_len'+str(index_list)] = len(posting_lists[index_list])
            name['list_pointer' + str(index_list)] = 0

        if len(posting_lists) > 1:
            while(min([name.get('list_pointer'+str(index_list)) < name.get('list_len'+str(index_list))
                       for index_list in range(len(posting_lists))])):
                wanted_item = name.get('list'+str(0))[name.get('list_pointer'+str(0))]
                flag = 1
                min_index = 0
                for i in range(1, len(posting_lists)):
                    if wanted_item > name.get('list'+str(i))[name.get('list_pointer' + str(i))]:
                        min_index = i
                        wanted_item = name.get('list'+str(i))[name.get('list_pointer' + str(i))]
                        flag = 0
                    if wanted_item < name.get('list'+str(i))[name.get('list_pointer' + str(i))]:
                        flag = 0
                if flag == 1:
                    for index_list in range(len(posting_lists)):
                        name['list_pointer' + str(index_list)] += 1
                    posting_merged.append(wanted_item)
                else:
                    name['list_pointer' + str(min_index)] += 1
        else:
            posting_merged = posting_lists[0]

        return posting_merged

    def merge_linear_skip(self, posting_lists: list):
        """
        Merge postings lists.
        Args:
            posting_lists (list): a list that contains postings lists to be merged.
        Returns:
            posting_merged (list): merged postings list.
        """
        posting_merged = list()
        name = locals()
        num_stride = 5

        posting_list_init = posting_lists[0]
        for i in range(1, len(posting_lists)):
            posting_list_init = self.skip_pointers(posting_list_init, posting_lists[i], num_stride)
        posting_merged = posting_list_init

        return posting_merged

    @staticmethod
    def skip_pointers(posting_list1: list, posting_list2: list, stride):
        posting_merged = list()
        list1_len = len(posting_list1)
        list1_pointer = 0

        list1_skip_len = int(len(posting_list1) / stride)
        list1_skip_list = [i*stride for i in range(list1_skip_len)]
        list1_skip_list.append(len(posting_list1)-1)
        list1_skip_pointer = 0

        list2_len = len(posting_list2)
        list2_pointer = 0

        list2_skip_len = int(len(posting_list2) / stride)
        list2_skip_list = [i*stride for i in range(list2_skip_len)]
        list2_skip_list.append(len(posting_list2) - 1)
        list2_skip_pointer = 0

        while min([list1_pointer < list1_len, list2_pointer < list2_len]):
            if posting_list1[list1_pointer] == posting_list2[list2_pointer]:
                posting_merged.append(posting_list1[list1_pointer])
                list1_pointer += 1
                list2_pointer += 1
            else:
                if posting_list1[list1_pointer] < posting_list2[list2_pointer]:

                    if (min([list1_skip_pointer < list1_skip_len,
                             posting_list1[list1_skip_list[list1_skip_pointer]] < posting_list2[list2_pointer]])):
                        while (min([list1_skip_pointer < list1_skip_len,
                                    posting_list1[list1_skip_list[list1_skip_pointer]] < posting_list2[list2_pointer]])):
                            list1_pointer = list1_skip_list[list1_skip_pointer]
                            list1_skip_pointer += 1
                    else:
                        list1_pointer += 1
                else:
                    if (min([list2_skip_pointer < list2_skip_len,
                             posting_list2[list2_skip_list[list2_skip_pointer]] < posting_list1[list1_pointer]])):
                        while (min([list2_skip_pointer < list2_skip_len,
                                    posting_list2[list2_skip_list[list2_skip_pointer]] < posting_list1[list1_pointer]])):
                            list2_pointer = list2_skip_list[list2_skip_pointer]
                            list2_skip_pointer += 1
                    else:
                        list2_pointer += 1

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
