import argparse
from components import *


parser = argparse.ArgumentParser(
    description='Information Retrieval System')
parser.add_argument('-d', '--dataset', default='HillaryEmails/',
                    help='Directory to the dataset.')


def main(args):
    dataset = Dataset(args.dataset)
    while True:
        query = input('Please input query for search (using space to separate multi queries):\n')
        if not query:
            continue
        start_time = time.time()
        output = dataset.query(query)
        time_used = time.time() - start_time
        if output:
            print('Num of Documents: {}\t Time: {:.4f}s'.format(len(output), time_used))
            print(output)
        else:
            print('Your search "{}" did not match any documents.'.format(query))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
