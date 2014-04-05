from text_analysis import Document, Corpus, Classifier

d1 = Document('kill kill bomb kidnap kidnap kidnap TV')
d2 = Document('kill bomb kidnap')
d3 = Document('kill bomb kidnap kidnap movie')

d4 = Document('bomb music music movie TV')
d5 = Document('kidnap music movie')
d6 = Document('music music movie movie')

terrorism = [d1, d2, d3]
entertainment = [d4, d5, d6]

corpus = Corpus()
for d in terrorism:
    corpus.add_document(d, 'terrorism')
for d in entertainment:
    corpus.add_document(d, 'entertainment')

classifier = Classifier(corpus)

for c in ['terrorism', 'entertainment']:
    print corpus.get_probability_class(c)
    print classifier.get_probability_word_with_class('kill', c)
    print classifier.get_probability_word_with_class('bomb', c)
    print classifier.get_probability_word_with_class('kidnap', c)
    print classifier.get_probability_word_with_class('music', c)
    print classifier.get_probability_word_with_class('movie', c)
    print classifier.get_probability_word_with_class('TV', c)
    print '----'

predict = 'kill kill bomb kidnap kidnap TV'
print classifier.classify(predict)



