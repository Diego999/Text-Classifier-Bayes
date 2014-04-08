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
        Return the number of success by class and the length of the validation set by class"""
    corpus = Corpus()
    for d in create_documents(training):
        corpus.add_document(d[1], d[0])

    classifier = Classifier(corpus)
    success = {}
    len_validation = {}
    for v in prepare_validation(validation):
        if v[0] not in success:
            success[v[0]] = 0
        if v[0] not in len_validation:
            len_validation[v[0]] = 0
        len_validation[v[0]] += 1

        if classifier.classify(v[1]) == v[0]:
            success[v[0]] += 1
    return success, len_validation


def avg(list):
    """ Return the average of a list """
    return sum(list)/float(len(list))


def display_intermediate_result(success, len_validation, classs):
    """ Display intermediate result for the classification """
    print 'Class ', classs, ' : ', "%.2f" % (100.0*success/float(len_validation)), '%% (%s/%s)' % (str(success), str(len_validation))


def display_final_result(success, len_validation):
    """ Display final result for the classification """
    print '\tTotal : ', '%.2f' % (100.0*success/float(len_validation)), '%'
    print ' '


def normal_validation():
    """ Train with normal validation """
    training, validation = create_training_validation_set(load_files())

    success, len_validation = validation_iteration(training, validation)
    for k in sorted(success.keys()):
        display_intermediate_result(success[k], len_validation[k], k)
    print ''
    display_final_result(sum(success.values()), sum(len_validation.values()))


def cross_validation():
    """ Train with cross validation """
    results = []
    len = []
    for i, sets in enumerate(create_training_validation_set_cross_validation(load_files())):
        success, len_validation = validation_iteration(sets[0], sets[1])
        print 'Set ', i+1
        for k in sorted(success.keys()):
            display_intermediate_result(success[k], len_validation[k], k)
        print ''
        results.append(sum(success.values()))
        len.append(sum(len_validation.values()))
    display_final_result(avg(results), avg(len))


def execute(f):
    globals()[f]()
    print f


if __name__ == '__main__':
    execute('cross_validation')
    execute('normal_validation')



