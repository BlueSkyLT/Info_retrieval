import argparse
from components import *


parser = argparse.ArgumentParser(
    description='Information Retrieval System')
parser.add_argument('-d', '--dataset', default='Novels/',
                    help='Directory to the dataset.')
parser.add_argument('-m', '--merge', default='merge_py',
                    help='Merge method. (merge_baseline, merge_linear or merge_linear_skip)')


def main(args):
    dataset = Dataset(args.dataset)
    while True:
        query = input('Please input query for search (using space to separate multi queries):\n')
        if not query:
            continue
        start_time = time.time()
        output = dataset.query(query, args.method)
        time_used = time.time() - start_time
        if output:
            for i, doc in enumerate(output):
                print('---------the {}-th result----------'.format(i))
                doc.print()
            print('------------------------------------')
            print('Num of Documents: {}\t Time: {:.4f}s'.format(len(output), time_used))
        else:
            print('Your search "{}" did not match any documents.'.format(query))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
