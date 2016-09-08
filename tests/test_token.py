import unittest

from xo import token


class IsTokenTestCase(unittest.TestCase):
    def test_when_given_x(self):
        self.assertTrue(token.istoken('x'))

    def test_when_given_o(self):
        self.assertTrue(token.istoken('o'))

    def test_when_given_anything_other_than_x_or_o(self):
        self.assertFalse(token.istoken(' '))
        self.assertFalse(token.istoken('.'))


class IsEmptyTestCase(unittest.TestCase):
    def test_when_given_x(self):
        self.assertFalse(token.isempty('x'))

    def test_when_given_o(self):
        self.assertFalse(token.isempty('o'))

    def test_when_given_anything_other_than_x_or_o(self):
        self.assertTrue(token.isempty(' '))
        self.assertTrue(token.isempty('.'))


class OtherTokenTestCase(unittest.TestCase):
    def test_when_given_x(self):
        self.assertEqual(token.other_token('x'), 'o')

    def test_when_given_o(self):
        self.assertEqual(token.other_token('o'), 'x')

    def test_when_given_anything_other_than_x_or_o(self):
        for piece in [' ', '.']:
            with self.assertRaisesRegex(ValueError, 'must be a token: {}'.format(piece)):
                token.other_token(piece)


class CanonicalPieceTestCase(unittest.TestCase):
    def test_when_given_x(self):
        self.assertEqual(token.canonical_piece('x'), 'x')

    def test_when_given_o(self):
        self.assertEqual(token.canonical_piece('o'), 'o')

    def test_when_given_anything_other_than_x_or_o(self):
        self.assertEqual(token.canonical_piece(' '), ' ')
        self.assertEqual(token.canonical_piece('.'), ' ')
