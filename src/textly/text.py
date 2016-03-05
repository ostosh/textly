import re

from nltk.stem import snowball
from nltk.corpus import words


class Word:
    nonalpha_regex = r'[^a-zA-Z]'
    numeric_regex = r'[0-9]'
    html_regex = r'<.*?>'
    stemmer = snowball.SnowballStemmer("english")
    word_corpus = set(words.words())
    stop_words = {
        'a', 'about', 'above', 'after', 'again',
        'against', 'all', 'am', 'an', 'and', 'any',
        'are', 'aren\'t', 'as', 'at', 'be', 'because',
        'been', 'before', 'being', 'below', 'between',
        'both', 'both', 'but', 'by', 'cant', 'cannot',
        'could', 'couldn\'t', 'did', 'didn\'t', 'do',
        'does', 'doesn\'t', 'doing', 'don\'t', 'down',
        'during', 'each', 'few', 'for', 'from',
        'further', 'had', 'hadn\'t', 'has', 'hasn\'t',
        'have', 'haven\'t', 'having', 'he', 'he\'d',
        'he\'ll', 'he\'s', 'her', 'here', 'here\'s',
        'hers', 'herself', 'him', 'himself', 'his'
        'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m',
        'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t',
        'it', 'it\'s', 'its', 'itself', 'let\'s',
        'me', 'more', 'most', 'mustn\'t', 'my',
        'myself', 'no', 'nor', 'not', 'of', 'off',
        'on', 'once', 'only', 'or', 'other', 'ought',
        'our', 'ours', 'ourselves', 'out', 'over',
        'own', 'same', 'shan\'t', 'she', 'she\'d',
        'she\'ll', 'she\'s', 'should', 'shouldn\'t',
        'so', 'some', 'such', 'than', 'that', 'that\'s',
        'the', 'their', 'theirs', 'them', 'themselves',
        'then', 'there', 'there\'s', 'these', 'they',
        'they\'d', 'they\'ll', 'they\'re', 'they\'ve',
        'this', 'those', 'through', 'to', 'too', 'under',
        'until', 'up', 'very', 'was', 'wasn\'t', 'we',
        'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were',
        'weren\'t', 'what', 'what\'s', 'when', 'when\'s',
        'where', 'where\'s', 'which', 'while', 'who',
        'who\'s', 'whom', 'why', 'why\'s', 'with',
        'with' 'won\'t', 'would', 'would', 'would',
        'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll',
        'you\'re', 'you\'ve', 'your', 'yours', 'yourself',
        'yourselves'
    }

    @staticmethod
    def strip(word):
        return re.sub(Word.html_regex, '', word)

    def sanitize(word):
        return re.sub(Word.nonalpha_regex, '', word)

    @staticmethod
    def normalize(word):
        return word.lower()

    @staticmethod
    def stem(word):
        return Word.stemmer.stem(word)

    @staticmethod
    def process(word):
        word = Word.normalize(word)
        word = Word.strip(word)
        word = Word.sanitize(word)
        word = Word.stem(word)
        return word

    @staticmethod
    def is_stop(word):
        return word in Word.stop_words

    @staticmethod
    def is_numeric(word):
        return re.match(Word.numeric_regex, word) is not None

    @staticmethod
    def is_html(word):
        return re.match(Word.html_regex, word) is not None

    def is_word(word):
        return word in Word.word_corpus


class Doc:
    @staticmethod
    def get_tokens(doc):
        for line in doc:
            for token in line.split():
                token = token.lower()
                if Word.is_stop(token):
                    continue
                if not Word.is_word(token):
                    continue
                if Word.is_numeric(token):
                    continue
                if Word.is_html(token):
                    continue
                token = Word.normalize(token)
                token = Word.sanitize(token)
                token = Word.stem(token)
                if not token == "":
                    yield token
