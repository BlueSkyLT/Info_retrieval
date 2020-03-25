import sys
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
 
ix = open_dir("indexdir")
 
# query_str is query string
query_str = sys.argv[1]

# 0: search by title
# 1: search by author
# 2: search by content
search_by = sys.argv[2]

# Top 'n' documents as result, default 10
topN = int(sys.argv[3])

# search by title

# search by author

# search by content 
with ix.searcher(weighting = scoring.Frequency) as searcher:
	query = QueryParser("content", ix.schema).parse(query_str)
	results = searcher.search(query,limit = topN)

	for i in range(topN):
		print(results[i]['title'], str(results[i].score), results[i]['textdata'])
