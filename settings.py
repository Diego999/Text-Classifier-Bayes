DATA_PATH = 'data/normal/'
DATA_TAGGED_PATH = 'data/tagged/'
CLASSES = ['pos', 'neg']
STOP_WORD_FILE_PATH = 'data/frenchST.txt'
SEPARATOR = '\t'

PERCENTAGE_FOR_TRAINING_SET = 0.8

STOP_WORDS = []
with open(STOP_WORD_FILE_PATH, 'r') as f:
    for l in f.read().splitlines():
        STOP_WORDS.append(l.decode('utf-8'))

""" cf http://www.ims.uni-stuttgart.de/institut/mitarbeiter/schmid/french-tagset.html """
ABBREVIATION = 'ABR'
ADJECTIVE = 'ADJ'
ADVERB = 'ADV'
DETERMINANT = 'DET:ART', 'DET:POS'
INTERJECTION = 'INT'
CONJUNCTION = 'KON'
PROPER_NAME = 'NAM'
NOUN = 'NOM'
NUMERAL = 'NUM'
PRONOUN = 'PRO', 'PRO:DEM', 'PRO:IND', 'PRO:PER', 'PRO:POS', 'PRO:REL'
PREPOSITION = 'RP', 'PRP:det'
PUNCTUATION = 'PUN', 'PUN:cit'
SENTENCE_TAG = 'SENT'
SYMBOL = 'SYM'
VERB = 'VER:cond', 'VER:futu', 'VER:impe', 'VER:impf', 'VER:infi', 'VER:pper', 'VER:ppre', 'VER:pres', \
       'VER:simp', 'VER:subi', 'VER:subp'
UNKNOWN = '<unknown>'

KEPT_TAGS = []  # Will be taken into account for classification
for c in [PROPER_NAME, NOUN, VERB]:
    KEPT_TAGS += list(c)

REFUSED_TAGS = []  # Won't be taken into account for the statistics
for c in [PUNCTUATION, SENTENCE_TAG, UNKNOWN]:
    REFUSED_TAGS += list(c)