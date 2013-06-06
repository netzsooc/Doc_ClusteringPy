'''
Created on 06/06/2013

@author: netzsooc
'''

class FreqTermCluster(object):
    '''
    classdocs
    '''


    def __init__(self,stopwords, ignorechars, docs):
        '''
        Constructor
        '''
        self._minsupp = .3
        self._dcount = 0
        self._stopwords =  stopwords
        self._ignorechars = ignorechars
        self.vocabulary =  set()
        self._get_vocabulary(docs)
        self.docs = {}
        self._set_docs(docs)
        self.freq_terms = set()
        self._set_freq_terms()


    def _get_terms(self, doc):
        return set([term.lower().
                    translate(term.maketrans('','',self._ignorechars))
                    for term in doc.split() 
                      if term.lower() not in self._stopwords])


    def _get_vocabulary(self, docs):
        for doc in docs:
            terms_in_doc = self._get_terms(doc)
            self.vocabulary = self.vocabulary.union(terms_in_doc)


    def _set_docs(self, docs):
        for doc in docs:
            self.docs["D" + str(self._dcount)] = self. _get_terms(doc)
            self._dcount += 1 


    def cov(self, termset):
        termset = set([termset])
        return set([d for d in self.docs 
                    if termset.issubset(self.docs[d])])


    def _set_freq_terms(self):
        f_terms = set([term for term in self.vocabulary if 
                        len(self.cov(term)) >= self._minsupp * len(self.docs)])
        self.freq_terms = self.freq_terms.union(f_terms)
            

def main(*args):
    docs = [
            "Human machine interface for ABC computer applications",
            "A survey of user opinion of computer system response time",
            "The EPS user interface management system",
            "System an human system engineering testing for EPS",
            "Relation of user perceived response time to error measurement",
            "The generation of random, binary, ordered trees",
            "The intersection graph of paths in trees",
            "Graph minors IV: Widths of trees and well-quasi-ordering",
            "Graph minors: A survey"
            ]
    docstopwords = ["the", "for", "of", "a", "and", "to", "in", "an"]
    ignorechars = ",:"
    test = FreqTermCluster(docstopwords,ignorechars, docs)
#     for doc in docs:
#         test.get_vocabulary(doc)

    print(test.vocabulary)
    print(test.docs["D0"])
    print(test.freq_terms)
    for term in test.freq_terms:
        print(test.cov(term))

if __name__ == "__main__": main()
    