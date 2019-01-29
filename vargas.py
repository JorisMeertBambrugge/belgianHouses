# functions to clean useless words
import nltk
from string import punctuation, digits
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# Eliminate words that you do not want in your sentences
def remove_tokens(tokens, remove_tokens = punctuation):
    return [token for token in tokens if token not in remove_tokens]

# reduce words to lowercase
def lowercase(tokens):
    return [token.lower() for token in tokens]

# remove fragmented words like: n't, 's
def remove_word_fragments(tokens):
    return [token for token in tokens if "'" not in token]

## Stemming
# Converts words to their 'base' form, for example:
# regular = house, housing, housed
# stemmed = hous, hous, hous
def stem(tokens):
    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def stopwords(tokens):
    from nltk.corpus import stopwords
    stops = stopwords.words('english')
    extra = ['...', 'promotion', 'review', 'collected', 'part']
    [stops.append(digit) for digit in digits]
    [stops.append(punct) for punct in punctuation]
    [stops.append(word) for word in extra]
    tokens = remove_tokens(tokens, stops)
    return tokens

# function that combines all of this commands into one
def clean_words(tokens, ommit = []):
    '''ommit options: lowercase, punct, stopwords, fragments, stem'''
    if 'lowercase' not in ommit:
        tokens = lowercase(tokens)
    
    if 'stopwords' not in ommit:
        tokens = stopwords(tokens)
        
    if 'fragments' not in ommit:
        tokens = remove_word_fragments(tokens)
        
    if 'stem' not in ommit:
        tokens = stem(tokens)
        
    return tokens
    