from math import log10
from settings import STOP_WORDS, KEPT_TAGS
from warnings import warn


class Document:
    """
    This class represent a document. This document could be a description or text parsing for a website
    """

    def __init__(self, text):
        self.statistics = dict()
        self.add_text(text)

    def get_statistics(self):
        """
        Return a dictionary contains the number of occurrence for all terms
        """
        return self.statistics

    def add_text(self, text):
        """
        Add the text to the document and update the statistics
        """
        for t in text:
            if len(t) == 3 and t[1] in KEPT_TAGS:
                w = t[2]
                if w not in STOP_WORDS:
                    if w in self.statistics:
                        self.statistics[w] += 1
                    else:
                        self.statistics[w] = 1


class Corpus:
    """
    Class represents a corpus, that contains a set of documents
    """

    def __init__(self):
        self.documents = list()
        self.documents_by_class = {}
        self.end_corpus = False

    def end_up_corpus(self):
        self.end_corpus = True

        final_by_class = {}
        for classs, documents in self.documents_by_class.items():
            if classs not in final_by_class:
                final_by_class[classs] = {}

            for d in [d.get_statistics() for d in documents]:
                for k, v in d.items():
                    if k not in final_by_class[classs]:
                        final_by_class[classs][k] = 0
                    final_by_class[classs][k] += v

        return final_by_class

    def get_classes(self):
        return self.documents_by_class.keys()

    def __contains__(self, item):
        return item in self.documents

    def add_document(self, document, classs):
        """
        Add a document in the corpus
        """
        if not self.end_corpus:
            if classs not in self.documents_by_class:
                self.documents_by_class[classs] = []
            self.documents_by_class[classs].append(document)

            self.documents.append(document)
        else:
            warn('The corpus is full ! The document hasn\'t been added !')

    def get_probability_class(self, classs):
        if classs not in self.documents_by_class:
            return 0.0
        else:
            return len(self.documents_by_class[classs])/sum(float(len(d)) for d in self.documents_by_class.values())


class Classifier:
    """
    Class whichs controls the corpus and classify text
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self.statistics_by_class = self.corpus.end_up_corpus()
        self.classes = corpus.get_classes()
        self.divisors = {}
        for c in self.classes:
            self.divisors[c] = sum(float(v) for v in self.statistics_by_class[c].values())

    def get_probability_word_with_class(self, word, classs):
        if classs not in self.classes:
            return 0.0

        divisor = (6.0+self.divisors[classs])
        if word not in self.statistics_by_class[classs]:
            return 1.0/divisor
        else:
            return (self.statistics_by_class[classs][word]+1.0)/divisor

    def classify(self, text):
        words = text.split()
        res = {}
        out = [self.classes[0], -float('Inf')]
        for c in self.classes:
            res[c] = 0.0
            for w in words:
                res[c] += log10(self.get_probability_word_with_class(w, c))
            res[c] += log10(self.corpus.get_probability_class(c))
            if res[c] > out[1]:
                out[0], out[1] = c, res[c]
        return out[0]

