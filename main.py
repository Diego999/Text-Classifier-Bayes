from text_analysis import Document, Corpus, Classifier
from settings import CLASSES, DATA_TAGGED_PATH, SEPARATOR, PERCENTAGE_FOR_TRAINING_SET
from os import listdir
from random import shuffle
import codecs


def load_files():
    """ We assume that all the text file are already "tagged" with TreeTagger """
    texts = {}
    for c in CLASSES:
        texts[c] = []
        path = DATA_TAGGED_PATH + c + '/'
        for f in listdir(path):
            if f.endswith('.txt'):
                with codecs.open(path + f, 'r', encoding='utf-8') as f:
                    texts[c].append([line.strip().split(SEPARATOR) for line in f.readlines()])
    return texts


def create_training_validation_set(texts):
    merge = []
    for k, v in texts.items():
        for vv in v:
            merge.append((k, vv))
    shuffle(merge)

    training = merge[0:int(PERCENTAGE_FOR_TRAINING_SET*len(merge))]
    validation = merge[int(PERCENTAGE_FOR_TRAINING_SET*len(merge)):]
    return training, validation


def create_documents(set):
    documents = []
    for s in set:
        documents.append((s[0], Document(s[1])))
    return documents


def prepare_validation(set):
    sets = []
    for s in set:
        text = ''
        for ss in s[1]:
            if len(ss) == 3:
                text += ss[2] + ' '
        sets.append((s[0], text))
    return sets

training, validation = create_training_validation_set(load_files())

corpus = Corpus()
for d in create_documents(training):
    corpus.add_document(d[1], d[0])

classifier = Classifier(corpus)
success = 0

for v in prepare_validation(validation):
    if classifier.classify(v[1])[0][0] == v[0]:
        success += 1.0
print 100.0*success/len(validation)



