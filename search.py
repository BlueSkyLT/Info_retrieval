import sys
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
 
ix = open_dir("indexdir")
 
# query_str is query string
query_str = sys.argv[1]
# query_str = 'song'

# search by title/author/content
search_by = sys.argv[2]
# search_by = 'author'

# Top 'n' documents as result, default 10
topN = int(sys.argv[3])
# topN = 2

# search by content 
with ix.searcher(weighting = scoring.Frequency) as searcher:
    query = QueryParser(search_by, ix.schema).parse(query_str)
    results = searcher.search(query, limit = topN)
    # number of results
    N_results = len(results)
    if N_results < 1:
        print('No matching results')
    elif N_results < topN:
        print('%i results found: ' % N_results)
        for i in range(N_results):
            print(results[i]['title'], str(results[i]['author']))
    # 		print(results[i]['title'], str(results[i].score), results[i]['textdata'])
    else:
        print('%i results found, displaying the top %i results: ' % (N_results, topN))
        for i in range(topN):
            print(results[i]['title'], str(results[i]['author']))