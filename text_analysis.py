from math import log10
from collections import OrderedDict
from settings import STOP_WORDS


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
        words = text.split()#TreeTagger().tag_text(text=text, all_tags=True)

        for w in words:
            if w not in STOP_WORDS:
                if w in self.statistics:
                    self.statistics[w] += 1
                else:
                    self.statistics[w] = 1

    def get_tf(self, term):
        """
        Compute the tf of a specific term
        """
        if term in self.statistics:
            occurrence = self.statistics[term]
            all_occurrences = 0
            for v in self.statistics.values():
                all_occurrences += v
            return float(occurrence)/float(all_occurrences)
        else:
            return 0.0


class Corpus:
    """
    Class represents a corpus, that contains a set of documents
    """

    def __init__(self):
        self.documents = list()
        self.classification = {}
        self.end_corpus = False

    def end_up_corpus(self):
        self.end_corpus = True

        final_by_class = {}
        for classs, documents in self.classification.items():
            if classs not in final_by_class:
                final_by_class[classs] = {}

            for d in [d.get_statistics() for d in documents]:
                for k, v in d.items():
                    print k, ' ', v
                    if k not in final_by_class[classs]:
                        final_by_class[classs][k] = 0
                    final_by_class[classs][k] += v

        return final_by_class

    def __contains__(self, item):
        return item in self.documents

    def add_document(self, document, classs):
        """
        Add a document in the corpus
        """
        if not self.end_corpus:
            if classs not in self.classification:
                self.classification[classs] = []
            self.classification[classs].append(document)

            self.documents.append(document)

    def get_idf(self, term):
        """
        Compute the idf of a specific term in the corpus
        """

        number_documents_with_term = 0
        for doc in self.documents:
            if doc.get_tf(term) != 0:
                number_documents_with_term += 1

        #  Mathematically the base of the function log is not important
        return log10(len(self.documents))/number_documents_with_term if number_documents_with_term != 0 else 1

    def get_probability_class(self, classs):
        if classs not in self.classification:
            return 0.0
        else:
            return len(self.classification[classs])/sum(float(len(d)) for d in self.classification.values())


class Classifier:
    def __init__(self, corpus):
        self.corpus = corpus
        self.final_by_class = self.corpus.end_up_corpus()
        self.classes = corpus.classification.keys()

    def get_probability_word_with_class(self, word, classs):
        if classs not in self.classes:
            return 0.0
        divisor = (6.0+sum(float(v) for v in self.final_by_class[classs].values()))
        if word not in self.final_by_class[classs]:
            return 1.0/divisor
        else:
            return (self.final_by_class[classs][word]+1.0)/divisor

    def classify(self, text):
        words = text.split()
        res = {}

        for c in self.classes:
            res[c] = 0.0
            for w in words:
                res[c] += log10(self.get_probability_word_with_class(w, c))
            res[c] += log10(self.corpus.get_probability_class(c))

        return OrderedDict(sorted(res.items(), key=lambda x: x[1], reverse=True)).items()

