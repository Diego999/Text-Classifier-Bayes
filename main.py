from text_analysis import Document, Corpus, Classifier
from settings import CLASSES, DATA_TAGGED_PATH, SEPARATOR, PERCENTAGE_FOR_TRAINING_SET, NUMBER_OF_SAMPLES
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


def merge_classes(texts):
    """ Merge all the documents from different classes into one """
    merge = []
    for k, v in texts.items():
        for vv in v:
            merge.append((k, vv))
    return merge


def create_training_validation_set(texts):
    """ Merge the documents and create a training set and a validation set
    with the specific option (PERCENTAGE_FOR_TRAINING_SET) """
    merge = merge_classes(texts)
    shuffle(merge)

    split = int(PERCENTAGE_FOR_TRAINING_SET*len(merge))
    return merge[0:split], merge[split:]


def create_training_validation_set_cross_validation(texts):
    """ Merge the documents and create set of training and validation sets for cross validation
    with the specific option (NUMBER_OF_SAMPLES) """
    merge = merge_classes(texts)
    shuffle(merge)
    step = len(merge)/NUMBER_OF_SAMPLES

    out = []
    for i in xrange(0, NUMBER_OF_SAMPLES-1):
        validation = merge[i*step:(i+1)*step]
        training = merge[:i*step] + merge[(i+1)*step:]
        out.append((training, validation))
    return out


def create_documents(set):
    """ Create as many documents as sets """
    documents = []
    for s in set:
        documents.append((s[0], Document(s[1])))
    return documents


def prepare_validation(set):
    """ Transform a document in a several sentences to test """
    sets = []
    for s in set:
        text = ''
        for ss in s[1]:
            if len(ss) == 3:
                text += ss[2] + ' '
        sets.append((s[0], text))
    return sets


def validation_iteration(training, validation):
    """ Create a corpus with the training set and classify the validation set.
        Return the percentage of success and the length of the validation set """
    corpus = Corpus()
    for d in create_documents(training):
        corpus.add_document(d[1], d[0])

    classifier = Classifier(corpus)
    success = 0
    for v in prepare_validation(validation):
        if classifier.classify(v[1]) == v[0]:
            success += 1.0
    return success, len(validation)


def normal_validation():
    """ Train with normal validation.
        Return the percentage of success and the length of the validation set"""
    training, validation = create_training_validation_set(load_files())
    return validation_iteration(training, validation)


def avg(list):
    """ Return the average of a list """
    return sum(list)/float(len(list))


def cross_validation():
    """ Train with cross validation
        Return the percentage of success and the length of the validation set"""
    results = []
    len = []
    for sets in create_training_validation_set_cross_validation(load_files()):
        success, len_validation = validation_iteration(sets[0], sets[1])
        results.append(success)
        len.append(len_validation)
    return avg(results), avg(len)


def execute(f):
    success, len_validation = globals()[f]()
    print f
    print 100.0*success/len_validation, '% : ', int(success), '/', int(len_validation)
    print ''

if __name__ == '__main__':
    execute('cross_validation')
    execute('normal_validation')



