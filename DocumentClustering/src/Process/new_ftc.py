import itertools
import math
from porterstemmer import Stemmer


def get_all_terms(D):
  T = []
  my_D = []
  my_Dict = {}
  n = 0
  for i in D:
    n += 1
    temp = []
    stopwords = ["a", "an", "and", "for", "of", "the", "to", "in"]
    for w in i.split():
      w = Stemmer()(w.lower().translate(w.maketrans(
			  '','',".!':,;()!")))
      if w in stopwords:
        continue
      
      temp.append(w)
      del(w)

    st = set(temp)
    T.extend(list(st))
    my_D.append(tuple(st))
    my_Dict[tuple(st)] = n
    del(temp)
    
  return list(set(T)), list(set(my_D)), my_Dict


def cov(S, D):
#     if not S: return tuple()
    if type(S) == str: S = [S]
    return [D[i] for i in range(len(D)) if set(S).issubset(D[i])]


def freq_terms(T, minsup, D):
  S = [x for x in T if len(cov(x, D)) >= (minsup * len(D))]
  F = []
  n = len(S)

  for i in range(1, n + 1):
    r = len(F)
    print("i =",i, "|F| =", len(F))
    F.extend([item for item in itertools.combinations(S, i) 
	      if len(cov(item, D)) >= (minsup * len(D))])
    if len(F) == r:
      break
    
  del(n)
  return F


def f(j, R):
  return len([i for i in R if set(i).issubset(j)])


#def EO(C, R, _D):
    #sm = 0

    #for d in C:
        #f = len([s for s in R if set(s).issubset(d)])
##         if f == 0:
##             f = 0.000001
        #sm += (-(1/f) * log(1/f))
    #return sm


def EO(C, R):
    return sum([(-(1/f(j, R))* math.log(1/f(j, R))) for j in C])


def card_sel(termsets, D):
    Ds = []
    print(termsets)
    for termset in termsets:
        coverage = cov(termset, D)
        
        if len(tuple(coverage)) > 1:
        
            for doc in coverage:
                if doc not in Ds:
                    Ds.append(doc)
    
        else:
            if not coverage in Ds:
                Ds.append(coverage)
    print(Ds)
    return len(Ds)

#
#docs = [
# 	"Human machine interface for ABC computer applications",
# 	"A survey of user opinion of computer system response time",
# 	"The EPS user interface management system",
# 	"System an human system engineering testing for EPS",
# 	"Relation of user perceived response time to error measurement",
# 	"The generation of random, binary, ordered trees",
# 	"The intersection graph of paths in trees",
# 	"Graph minors IV: Widths of trees and well-quasi-ordering",
# 	"Graph minors: itemA survey"
#        ]
docs = []
with open("/home/netzsooc/Documents/just_abstracts.txt") as f:
    for line in f:
        docs.append(line)
#docs = [l.strip() for l in open("/home/netzsooc/Documents/just_abstracts.txt")]
T, D, DicD = get_all_terms(docs)
for i in range(len(D)):
    DicD[D[i]] = str(i + 1)
minsup = .2
sel_terms = []
n = len(D)
D1 = D[:]
rem_terms = freq_terms(T, minsup, D)
print(card_sel(rem_terms, D))
card = card_sel(sel_terms, D)
cluster_cands = {}
for term in rem_terms:
    cluster_cands[term] = cov(term, D)
 
while card != n:
    cands = []
     
    for item in rem_terms:
        #Calculate overlap for set
        C = cluster_cands[item]
        x = EO(C, rem_terms)
        cands.append((x, item))
           
    #Get the best cluster candidate
#     if len(cands) == 0: break
    cands.sort()
    best_cand = cands[0][1]
    sel_terms.append(best_cand)
    i = 0
    while i < len(sel_terms):
        if set(sel_terms[i]).issubset(best_cand):
            if sel_terms[i] != best_cand:
                sel_terms.remove(sel_terms[i])
                continue
        i += 1
    card = card_sel(sel_terms, D1)
    print(card)
    rem_terms.remove(best_cand)
   
    #Remove all docs in cov(best_cand) from D and from all coverages
    for doc in cov(best_cand, D):
        D.remove(doc)
        for ccand in cluster_cands.keys():
            if doc in cluster_cands[ccand]:
                cluster_cands[ccand].remove(doc)
#     print(sel_terms)
    
print(D)
for i in sel_terms:
    print(i, cov(i, D1))
