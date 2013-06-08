import itertools
import math
from porterstemmer import Stemmer


def get_all_terms(D):
  T = []
  my_D = []
  
  for i in range(len(D)):
    temp = []
    stopwords = ["a", "an", "and", "for", "of", "the", "to", "in"]
    for w in D[i].split():
      w = Stemmer()(w.lower().translate(w.maketrans(
			  '','',".!':,;()!")))
      if w in stopwords:
        continue
      
      temp.append(w)
      del(w)
      
    T.extend(list(set(temp)))
    my_D.append(tuple(set(temp)))
    del(temp)
    
  return list(set(T)), list(set(my_D))


def cov(S, D):
  if not S: return tuple()
  if type(S) == str: S = [S]
  return tuple([D[i] for i in range(len(D)) if set(S).issubset(D[i])])


def freq_terms(T, minsup, D):
  #S = [x for x in T if len(cov(x, D)) >= (minsup * len(D))]
  F = []
  n = len(T)

  for i in range(1, n + 1):
    r = len(F)
    print("i =",i, "|F| =", len(F))
    F.extend([item for item in itertools.combinations(T, i) 
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
  
  for termset in termsets:
    coverage = cov(termset, D)
    
    if len(tuple(coverage)) > 1:
      
      for doc in coverage:
        if doc not in Ds:
          Ds.append(doc)

    else:
      if not coverage in Ds:
        Ds.append(coverage)

  return len(Ds)


docs = [
	"Human machine interface for ABC computer applications",
	"A survey of user opinion of computer system response time",
	"The EPS user interface management system",
	"System an human system engineering testing for EPS",
	"Relation of user perceived response time to error measurement",
	"The generation of random, binary, ordered trees",
	"The intersection graph of paths in trees",
	"Graph minors IV: Widths of trees and well-quasi-ordering",
	"Graph minors: itemA survey"
       ]
T, D = get_all_terms(docs)
minsup = .2
sel_terms = []
n = len(D)
rem_terms = freq_terms(T, minsup, D)

while card_sel(sel_terms, D) != n:
  cands = []
  
  for item in rem_terms:
    #Calculate overlap for set
    C = cov(item, D)
    x = EO(C, rem_terms)
    cands.append((x, item))
  #Get the best cluster candidate
  best_cand = min(cands)[1]
  sel_terms = sel_terms.append(best_cand)
  rem_terms.remove(best_cand)

  #Remove all docs in cov(best_cand) from D and from all coverages
  for doc in cov(best_cand, D):
    D.remove(doc)
  print(sel_terms)
    
print(sel_terms)