from numpy import zeros, asarray
from numpy import sum as npsum
from scipy.linalg import svd
from math import log 
from porterstemmer import Stemmer


class LSA(object):


  def __init__(self, stopwords, ignorechars):
    self._stopwords =  stopwords
    self._ignorechars = ignorechars
    self._doc_count = 0
    self.vocabulary =  {}


  def get_vocab(self, doc, stem=True):
    terms = doc.split()

    for term in terms:
      term = term.lower().translate(term.maketrans('','',self._ignorechars))

      if term in self._stopwords:
        continue

      if stem:
        term = Stemmer()(term)

      self.vocabulary.setdefault(term, []).append(self._doc_count)

    self._doc_count += 1


  def build_term_matrix(self):
    terms = sorted([term for term in self.vocabulary.keys() 
                          if len(self.vocabulary[term]) > 1])
    self.term_matrix = zeros([len(terms), self._doc_count])

    for i,term in enumerate(terms):

      for document in self.vocabulary[term]:
        self.term_matrix[i, document] += 1

    print(terms)


  def get_tfidf(self):
    terms_per_doc = npsum(self.term_matrix, axis=0)
    docs_per_term = npsum(asarray(self.term_matrix > 0, 'i'), axis=1)
    rows, cols = self.term_matrix.shape

    for i in range(rows):

      for j in range(cols):
        self.term_matrix[i, j] = ((self.term_matrix[i, j] / terms_per_doc[j]) *
                                   log(cols / docs_per_term[j]))


  def calc_svd(self):
    self.U, self.S, self.Vt = svd(self.term_matrix)


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
  stopwords = ["the", "for", "of", "a", "and", "to", "in"]
  ignorechars = ",:"
  test = LSA(stopwords, ignorechars)

  for doc in docs:
    test.get_vocab(doc, False)

  test.build_term_matrix()
  test.calc_svd()
  print(test.term_matrix)
  print(test.U)
  print(test.S)
  print(test.Vt)


if __name__ == "__main__": main()
