DATA_PATH = 'data/normal/pos'
DATA_TAGGED_PATH = 'data/tagged/'
CLASSES = ['pos', 'neg']
STOP_WORD_FILE_PATH = 'data/frenchST.txt'

STOP_WORDS = []
with open(STOP_WORD_FILE_PATH, 'r') as f:
    for l in f.read().splitlines():
        STOP_WORDS.append(l.decode('utf-8'))