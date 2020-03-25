import os, sys
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.analysis import LanguageAnalyzer
from get_content import *

def createSearchableData(DIR):   
    '''
    Schema: 
        title: title of the novel, 
        path(as ID), 
        author: author of the novel,
        content(tokens, stemmed, indexed but not stored),
        textdata (stored full novel content)
    '''
    # use English Snowball stemmer
    stem_ana = LanguageAnalyzer("en")
    schema = Schema(title = TEXT(stored = True), path = ID(stored = True), author = ID(stored = True), content = TEXT(analyzer = stem_ana, sortable = True), textdata = TEXT(stored = True))
    
    # directory for the index
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
 
    # Creating a index writer to add document as per schema
    ix = create_in("indexdir", schema)
    writer = ix.writer()
 
    filepaths = [os.path.join(DIR,i) for i in os.listdir(DIR)]
    
    for path in filepaths:
        print(path)
        # get title, author and content from text
        title, author, text = get_content(path)
        writer.add_document(title = title, author = author, path = path, content = text, textdata = text)
    writer.commit()

# read the da
dataset = sys.argv[1]
createSearchableData(dataset)