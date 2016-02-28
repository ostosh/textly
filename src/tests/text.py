import unittest

from textly.text import Word


class TestText(unittest.TestCase):

    def test_strip(self):
        # spec removes all html tags according to niave regex
        self.assertEqual('Cant', Word.strip('Cant'))
        self.assertEqual('', Word.strip('<div>'))
        self.assertEqual('', Word.strip('<>'))
        self.assertEqual('test', Word.strip('<div>test</div>'))

    def test_sanitize(self):
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

    def test_normalize(self):
        # spec returns all strings in lowercase form
        self.assertEqual('and', Word.normalize('AND'))
        self.assertEqual('and', Word.normalize('and'))
        self.assertEqual('and', Word.normalize('aNd'))
        self.assertEqual('and', Word.normalize('anD'))

    def test_stem(self):
        # spec stems words according to snowball algorithm
        self.assertEqual('semant', Word.stem('semantically'))
        self.assertEqual('destruct', Word.stem('destructiveness'))
        self.assertEqual('recogn', Word.stem('recognizing'))

        # spec returns empty string for empty string
        self.assertEqual('', Word.stem(''))

    def test_is_stop(self):
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


