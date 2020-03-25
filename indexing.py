import os, sys
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.analysis import StemmingAnalyzer

def createSearchableData(DIR):   
    '''
    Schema definition: 
        title(name of file), 
        path(as ID), 
        content(indexed
    but not stored),
        textdata (stored text content)
        Date?
        Subject?
    '''
    stem_ana = StemmingAnalyzer()
    schema = Schema(title=TEXT(stored = True), path = ID(stored=True), content = TEXT(analyzer = stem_ana), textdata = TEXT(stored = True), date = DATETIME(sortable = True))
    
    # directory for the index
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
 
    # Creating a index writer to add document as per schema
    ix = create_in("indexdir",schema)
    writer = ix.writer()
 
    filepaths = [os.path.join(DIR,i) for i in os.listdir(DIR)]
    for path in filepaths:
        fp = open(path,'r', encoding = "utf8", errors = 'ignore')
        print(path)
        text = fp.read()
        writer.add_document(title = path.split('/')[1], path = path, content = text, textdata = text)   
        fp.close()
    writer.commit()

# read the dataset
dataset = sys.argv[1]
createSearchableData(dataset)