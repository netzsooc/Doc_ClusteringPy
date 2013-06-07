'''
Created on Jun 6, 2013

@author: netzsooc
'''
from itertools import combinations
from math import log
from prepro import get_vocabulary, get_terms, cov, index_words


class FTC(object):
    
    F = [] #Frequent Term Sets
    selected_terms = set() 


    def __init__(self, D, minsup, enc, T):
        n = len(D)
        rem_term_sets = get_all_freq_term_sets(T, D, enc, minsup)
    #     print(len(sel_terms))
        while len(cov(sel_terms, D)) != n:
            candidates = []
            for t in rem_term_sets:
                c = cov(t, D)
                eo = EO(c, rem_term_sets, D)
                candidates.append((eo,t))
            best_cand = min(candidates)
    #         print(best_cand)
            sel_terms.union(best_cand[1])
            rem_term_sets.remove(best_cand[1])
            
            Ds = [d for d in cov(best_cand[1], D)]
            for d in Ds:
                D.pop(d, None)
    
        for i in range(len(sel_terms)):
            sel_terms[i] = (sel_terms[i], cov(sel_terms[i], D))
        return sel_terms


    def _get_all_freq_term_sets(T, D, enc, minsup):
        S = set([enc[t] for t in T if len(cov({enc[t]}, D)) >= minsup * len(D)])
        F = []
        for i in range(1, len(S) + 1):
            F += [set(j) for j in combinations(S,i)]
        i = 0
        while i < len(F):
            term = F[i]
            if len(cov(term, D)) >= minsup * len(D):
                i += 1
                continue
            else:
                F.remove(term)
        return F    


def EO(C, R, D):
    sm = 0

    for d in C:
        f = len([s for s in R if s.issubset(D[d])])
#         if f == 0:
#             f = 0.000001
        sm += (-(1/f) * log(1/f))

    return sm


def main(*args):
    
    minsup = .2
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
#     docs = [title for title in open("/home/netzsooc/Documents/infotec/"\
#                                         "Investigacion/justTitles.txt")]
    
    print("getting vocabulary")
    T = get_vocabulary(docs)
    print("building encoding and decoding dictionaries")
    enc = index_words(T)
#     dec = dict([(v,k) for k,v in enc.items()])
    D = {}
    print("Building D")
    for i in range(len(docs)):
        D["D" + str(i)] = get_terms(docs[i], enc)
    print("Done")
    print(len(T))
    print("getting FTC")
    out = FTC(D, minsup, enc, T)
    print("done")
#     print("going out")
#     print(out)
#     print("goodbye")
#     F = get_all_freq_term_sets(T, D, enc, minsup)
#     print(F)
#     print(len(F))
#     temp = []
#     for term in F:
#         for i in (cov(term, D)):
#             temp.append(i)
#             
#     temp = list(set(temp))
#      
#     print("temp_set =",len(temp), "docs =", len(docs))    
#     print(len(temp) == len(docs))
#     print(temp)
#     print(F)

    
if __name__ == "__main__": main()