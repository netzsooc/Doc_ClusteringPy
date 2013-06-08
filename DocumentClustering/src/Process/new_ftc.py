import itertools
import math
from porterstemmer import Stemmer


def get_all_terms(D):
  T = []
  my_D = []
  
  for i in range(len(D)):
    temp = []
    stopwords = ["a", "an", "and", "for", "of", "the", "to"]
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
    
  return T, my_D


def cov(S, D):
  if not S: return tuple()
  if type(S) == str: S = [S]
  return tuple([D[i] for i in range(len(D)) if set(S).issubset(D[i])])


def freq_terms(T, minsup, D):
  F = [x for x in T if len(cov(x, D)) >= (minsup * len(D))]
  n = len(F)

  for i in range(1, n + 1):

    for j in itertools.combinations(F, i):

      if len(cov(j, D)) >= (minsup * len(D)):
        F.append(j)

    del(j)
  #del(i)

  del(n)
  return F


def f(j, R):
  return len([i for i in R if set(i).issubset(j)])


def EO(C, R):
  return sum([(-(1/f(j, R))* math.log(1/f(j, R))) for j in C])


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
T, D = get_all_terms(docs)
minsup = .2
sel_terms = []
n = len(D)
#rem_terms = freq_terms(T, minsup, D)
