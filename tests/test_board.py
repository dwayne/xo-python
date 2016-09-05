import unittest

from xo.board import Board


class BoardCreationTestCase(unittest.TestCase):
    def test_when_layout_is_empty(self):
        self.assertEqual(str(Board.fromstring()), '.........')

    def test_when_layout_contains_non_pieces(self):
        self.assertEqual(str(Board.fromstring('x.o-*x1o^')), 'x.o..x.o.')

    def test_when_layout_is_non_empty_but_shorter_than_9_characters(self):
        self.assertEqual(str(Board.fromstring('x')), 'x........')

    def test_when_layout_is_longer_than_9_characters(self):
        self.assertEqual(str(Board.fromstring('x       oxoxo')), 'x.......o')


class BoardGetItemTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board.fromstring('x.o.o.x.x')

    def test_when_board_contains_position(self):
        self.assertEqual(self.board[1, 1], 'x')
        self.assertEqual(self.board[1, 2], ' ')
        self.assertEqual(self.board[1, 3], 'o')
        self.assertEqual(self.board[2, 1], ' ')
        self.assertEqual(self.board[2, 2], 'o')
        self.assertEqual(self.board[2, 3], ' ')
        self.assertEqual(self.board[3, 1], 'x')
        self.assertEqual(self.board[3, 2], ' ')
        self.assertEqual(self.board[3, 3], 'x')

    def test_when_board_does_not_contain_position(self):
        with self.assertRaisesRegex(IndexError, 'position out of bounds: 0, 0'):
            self.board[0, 0]


class BoardSetItemTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board.fromstring()

    def test_when_board_contains_position(self):
        self.board[1, 1] = 'o'
        self.board[1, 3] = 'x'
        self.board[2, 2] = 'o'
        self.board[3, 3] = 'x'

        self.assertEqual(str(self.board), 'o.x.o...x')

    def test_when_board_does_not_contain_position(self):
        with self.assertRaisesRegex(IndexError, 'position out of bounds: 2, 4'):
            self.board[2, 4] = 'o'


class BoardIterationTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board.fromstring('x.xo..')

    def test_it_iterates_over_each_piece_in_row_major_order(self):
        expected = [
            (1, 1, 'x'),
            (1, 2, ' '),
            (1, 3, 'x'),
            (2, 1, 'o'),
            (2, 2, ' '),
            (2, 3, ' '),
            (3, 1, ' '),
            (3, 2, ' '),
            (3, 3, ' ')
        ]

        for i, (r, c, piece) in enumerate(self.board):
            with self.subTest(r=r, c=c):
                self.assertEqual((r, c, piece), expected[i])


class BoardToASCIITestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board.fromstring('x...o')

    def test_it_outputs_a_multiline_string_representation(self):
        self.assertEqual(
            self.board.toascii(),
            ' x |   |   \n'
            '---+---+---\n'
            '   | o |   \n'
            '---+---+---\n'
            '   |   |   '
        )
