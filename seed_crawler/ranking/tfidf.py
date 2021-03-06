import sys
import nltk
import math
import operator
import numpy as np
from os.path import exists

class tfidf:
    def __init__(self, opt_docs = None):
        self.documents = {}
        self.corpus_dict = {}
        self.idf = {}
        self.tfidfVector = {}
        self.corpus_tf = {}
        if opt_docs != None:
          self.process(opt_docs)

    def term_frequency(self):
        return self.documents

    def getFreqDist(self, text):
        return nltk.probability.FreqDist(text)

    def getIdf(self):
        num = float(len(self.documents))
        for word in self.corpus_dict:
            den = self.corpus_dict[word]
            if den == 0:
                den = den + 1

            self.idf[word] = math.log(num/den)

    def getTfidf(self):
        for url in self.documents.keys():
            tf = self.documents[url]
            doc_tfidf = {}
            for word in tf:
                doc_tfidf[word] = tf[word] * self.idf[word]
            self.tfidfVector[url] = doc_tfidf

    def getTopTerms(self,top):
        corpus = sorted(self.corpus_tf.items(), key=operator.itemgetter(1),reverse=True)
        return [x[0] for x in corpus[0:top]]

    def getIndex(self, terms):
        corpus = sorted(self.corpus_tf.items(), key=operator.itemgetter(1),reverse=True)
        corpus_keys = [x[0] for x in corpus]
        index = []
        for term in terms:
            index.append(corpus_keys.index(term.strip()))
        return index

    def getTfidfArray(self):
        corpus = sorted(self.corpus_tf.items(), key=operator.itemgetter(1),reverse=True)
        urls = self.tfidfVector.keys()
        data = np.ndarray(shape=(len(urls),len(corpus)))
        index_i = 0
        for url in urls:
            vect = self.tfidfVector[url]
            index_j = 0
            for [word, count] in corpus:
                data[index_i,index_j] = vect.get(word, 0.0)
                index_j = index_j + 1 
            index_i = index_i + 1
        return [urls, corpus, data]

    def getTfArray(self):
        corpus = sorted(self.corpus_tf.items(), key=operator.itemgetter(1),reverse=True)
        urls = self.documents.keys()
        data = np.ndarray(shape=(len(urls),len(corpus)))
        index_i = 0
        for url in urls:
            tf = self.documents[url]
            index_j = 0
            for [word, count] in corpus:
                data[index_i,index_j] = tf.get(word, 0.0)
                index_j = index_j + 1 
            index_i = index_i + 1
        return [urls, corpus, data]
    
    def getURLs(self, args):
        return [self.documents[x][0] for x in args]

    def getTerms(self, args):
        corpus = sorted(self.corpus_tf.items(), key=operator.itemgetter(1),reverse=True)
        return [corpus[x][0] for x in args]
        
    def process(self, documents):
        for url in documents.keys():
            content = documents[url]
            tokens = content.split(" ");
            text = [ word.strip().strip('"') for word in nltk.Text(tokens)]

            fdist = self.getFreqDist(text)

            N = fdist.N()
            for word in fdist:
                self.corpus_dict[word] = self.corpus_dict.get(word,0.0) + 1.0
                self.corpus_tf[word] = self.corpus_tf.get(word,0.0) + fdist[word]
                fdist[word] = fdist[word] / float(N)
            self.documents[url]=fdist
        self.getIdf()
        self.getTfidf()            
                    


