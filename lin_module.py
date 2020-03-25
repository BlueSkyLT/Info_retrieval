from nltk.stem.snowball import SnowballStemmer

def stemming(content):
    '''
    2. Linguistic Modules
    This component will perform two simple linguistic transformations on tokens: removing all punctuation symbols (!@#$%^&*()-_=+'`~ ":;|/.,?[]{}<>), lowercasing and stemming. For every token in the input list, we will first lowercase it, and then stem it, and finally add the result to the output list.
    '''
    stemmer = SnowballStemmer("english")
    stemmer.stem(content)