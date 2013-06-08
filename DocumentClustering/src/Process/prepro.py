'''
Created on Jun 6, 2013

@author: netzsooc
'''
from porterstemmer import Stemmer

stop = ["the", "for", "of", "a", "and", "to", "in", "an"]
ignore = "(),:'\""


def get_terms(doc, index=None, ignorechars=ignore, stopwords=stop):
    if index:
        return set([index[Stemmer()(term.lower().
                translate(term.maketrans('','',ignorechars)))]
                for term in doc.split() 
                    if term.lower() not in stopwords])
    return set([Stemmer()(term.lower().
                translate(term.maketrans('','',ignorechars)))
                for term in doc.split() 
                    if term.lower() not in stopwords])


def index_words(termset):
    my_map = {}
    i = 0
    for term in termset:
        my_map[term] = i
        i += 1
    return my_map


def get_vocabulary(docs, ignorechars=ignore, stopwords=stop):
    vocab = set()
    for doc in docs:
        terms_in_doc = get_terms(doc, False, ignorechars, stopwords)
        vocab = vocab.union(terms_in_doc)
    return vocab


def cov(term_set, docs):
    if len(term_set) == 0:
        return set()
    return set([d for d in docs.keys()
                if term_set.issubset(docs[d])])