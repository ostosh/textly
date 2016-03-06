import unittest
import os

from textly.text import Word
from textly.text import Doc


class TestText(unittest.TestCase):

    def test_word_strip(self):
        # spec removes all html tags according to niave regex
        self.assertEqual('Cant', Word.strip('Cant'))
        self.assertEqual('', Word.strip('<div>'))
        self.assertEqual('', Word.strip('<>'))
        self.assertEqual('test', Word.strip('<div>test</div>'))

    def test_word_sanitize(self):
        # spec returns all strings with alpha characters only
        self.assertEqual('Cant', Word.sanitize('Can\'t'))
        self.assertEqual('cannot', Word.sanitize('cannot'))
        self.assertEqual('Yu', Word.sanitize('Y*u'))
        self.assertEqual('', Word.sanitize('<>&$()31$(*'))
        self.assertEqual('', Word.sanitize(' '))
        self.assertEqual('', Word.sanitize('1234567890'))
        self.assertEqual('', Word.sanitize('`~!@#$%^&*()_+=-/?,<.>\'";:[{]}\|'))
        self.assertEqual('Lt', Word.sanitize('L33t'))
        self.assertEqual('', Word.sanitize(''))

    def test_word_normalize(self):
        # spec returns all strings in lowercase form
        self.assertEqual('and', Word.normalize('AND'))
        self.assertEqual('and', Word.normalize('and'))
        self.assertEqual('and', Word.normalize('aNd'))
        self.assertEqual('and', Word.normalize('anD'))

    def test_word_stem(self):
        # spec stems words according to snowball algorithm
        self.assertEqual('semant', Word.stem('semantically'))
        self.assertEqual('destruct', Word.stem('destructiveness'))
        self.assertEqual('recogn', Word.stem('recognizing'))

        # spec returns empty string for empty string
        self.assertEqual('', Word.stem(''))

    def test_word_is_stop(self):
        # spec matches stop words
        self.assertEqual(True, Word.is_stop('the'))
        self.assertEqual(True, Word.is_stop('do'))
        self.assertEqual(True, Word.is_stop('and'))

        # spec assumes lowercase
        self.assertEqual(False, Word.is_stop('THE'))
        self.assertEqual(False, Word.is_stop('DO'))
        self.assertEqual(False, Word.is_stop('AND'))

        # spec does not match non-stop words
        self.assertEqual(False, Word.is_stop('EXITED'))
        self.assertEqual(False, Word.is_stop('exit'))
        self.assertEqual(False, Word.is_stop('Company'))
        self.assertEqual(False, Word.is_stop('Successful'))
        self.assertEqual(False, Word.is_stop(''))

    def test_doc_get_tokens(self):
        # spec extracts valid english non-stop words in lower case form from given document
        word_tokens = {'success', 'WIN', 'wrong',  'BLah', 'test', 'BiGger', 'successful'}
        stop_word_tokens = {'the', 'is', 'isn\'t', 'he', 'she'}
        non_word_tokens = {'3442', 'ab1ad', 'uuss,a', '!*#)', '  ', 'zz', 'the'}

        test_file = open('test.txt', 'w+')
        [test_file.write(word + ' ') for word in word_tokens]
        [test_file.write(stop_word + ' ') for stop_word in stop_word_tokens]
        [test_file.write(non_word + ' ') for non_word in non_word_tokens]

        test_file.seek(0)
        test_tokens = Doc.get_tokens(test_file)

        test_control_tokens = {'bigger', 'wrong', 'blah', 'win', 'test', 'success'}
        for test_token in test_tokens:
            self.assertEqual(True, test_token in test_control_tokens)
        os.remove('test.txt')


