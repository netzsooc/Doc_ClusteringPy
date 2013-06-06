'''
Created on Jun 6, 2013

@author: netzsooc
'''

class FTC(object):
    '''
    classdocs
    '''
    
    
    def __init__(self, docs, minsup):
        '''
        Constructor
        '''
        self.selected_term_sets = {}
        self.remaining_term_sets = self.get_freq_termsets(docs, minsup)
        doc_card = len(docs)


    def get_freq_termsets(self, docs, minsup):
        pass


def main(*args):
    
    minsup = .3
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
#     docstopwords = ["the", "for", "of", "a", "and", "to", "in", "an"]
#     ignorechars = ",:"
    test = FTC(docs, minsup)
#     for doc in docs:
#         test.get_vocabulary(doc)

    print(test.vocabulary)
    print(test.docs["D0"])
    print(test.freq_terms)
    for term in test.freq_terms:
        print(test.cov(term))

if __name__ == "__main__": main()