'''
Created on Jun 6, 2013

@author: netzsooc
'''

from prepro import get_vocabulary, get_terms, cov, index_words



def main(*args):
    
    minsup = .05
#     docs = [
#             "Human machine interface for ABC computer applications",
#             "A survey of user opinion of computer system response time",
#             "The EPS user interface management system",
#             "System an human system engineering testing for EPS",
#             "Relation of user perceived response time to error measurement",
#             "The generation of random, binary, ordered trees",
#             "The intersection graph of paths in trees",
#             "Graph minors IV: Widths of trees and well-quasi-ordering",
#             "Graph minors: A survey"
#             ]
    docs = [title for title in open("/home/netzsooc/Documents/infotec/Investigacion/cleanAbstracts.txt")]
    

    T = get_vocabulary(docs)
    enc = index_words(T)
    dec = dict([(v,k) for k,v in enc.items()])
    D = {}
    for i in range(len(docs)):
        D["D" + str(i)] = get_terms(docs[i], enc)
    print(len(T))
    F = set([enc[i] for i in T if len(cov({enc[i]}, D)) >= minsup * len(D)])
    print(len(F))

    
if __name__ == "__main__": main()