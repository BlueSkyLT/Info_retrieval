import argparse
from components import *
from itertools import chain


parser = argparse.ArgumentParser(
    description='Information Retrieval System')
parser.add_argument('-d', '--dataset', default='HillaryEmails/',
                    help='Directory to the dataset.')


def main(args):
    files = get_files(args.dataset)
    file_token_list = list(list())  # containing token list for each file
    for file in files[:10]:  # TODO for test
        with open(file) as f:
            file_token_list.append(linguistic(tokenization(f.read(), file)))
    all_token_list = list(chain.from_iterable(file_token_list))  # containing tokens from all documents
    sorting(all_token_list)  # in-place sorting, save memory
    posting = Posting()
    for token in all_token_list:
        posting.add(token)
    # posting.sort()
    return


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
