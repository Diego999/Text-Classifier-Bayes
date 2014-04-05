from text_analysis import Document, Corpus, Classifier

d1 = Document([['kill', 'VER:infi', 'kill'],
               ['kill', 'VER:infi', 'kill'],
               ['bomb', 'NOM', 'bomb'],
               ['kidnap', 'VER:infi', 'kidnap'],
               ['kidnap', 'VER:infi', 'kidnap'],
               ['kidnap', 'VER:infi', 'kidnap'],
               ['TV', 'NOM', 'TV']])

d2 = Document([['kill', 'VER:infi', 'kill'],
               ['bomb', 'NOM', 'bomb'],
               ['kidnap', 'VER:infi', 'kidnap']])

d3 = Document([['kill', 'VER:infi', 'kill'],
               ['bomb', 'NOM', 'bomb'],
               ['kidnap', 'VER:infi', 'kidnap'],
               ['kidnap', 'VER:infi', 'kidnap'],
               ['movie', 'NOM', 'movie']])

d4 = Document([['bomb', 'NOM', 'bomb'],
               ['music', 'NOM', 'music'],
               ['music', 'NOM', 'music'],
               ['TV', 'NOM', 'TV'],
               ['movie', 'NOM', 'movie']])

d5 = Document([['kidnap', 'VER:infi', 'kidnap'],
               ['music', 'NOM', 'music'],
               ['movie', 'NOM', 'movie']])

d6 = Document([['music', 'NOM', 'music'],
               ['music', 'NOM', 'music'],
               ['movie', 'NOM', 'movie'],
               ['movie', 'NOM', 'movie']])

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



