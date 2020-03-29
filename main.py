import argparse
from components import *


parser = argparse.ArgumentParser(
    description='Information Retrieval System')
parser.add_argument('-d', '--dataset', default='HillaryEmails',
                    help='Directory to the dataset.')
parser.add_argument('-m', '--merge', default='merge_py',
                    help='Merge method. (merge_baseline, merge_linear or merge_linear_skip)')


def main(args):
    dataset = Dataset(args.dataset)
    while True:
        query = input('Please input query for search (using space to separate multi queries):\n')
        if not query:
            continue
        output, time_used = dataset.query(query, args.merge)
        if output:
            for i, doc in enumerate(output, 1):
                print('---------the {}-th result----------'.format(i))
                doc.print()
            print('------------------------------------')
            print('Num of Documents: {}\t Time: {:.4f}s'.format(len(output), time_used))
        else:
            print('Your search "{}" did not match any documents.'.format(query))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
