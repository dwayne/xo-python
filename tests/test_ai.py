import unittest

import xo.ai as ai
from xo.board import Board


class OpeningGameTestCase(unittest.TestCase):
    def test_xeeeeeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('x'), 'o').positions,
            [(2, 2)]
        )

    def test_exeeeeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('.x'), 'o').positions,
            [(1, 1), (1, 3), (2, 2), (3, 2)]
        )

    def test_eeeexeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('....x'), 'o').positions,
            [(1, 1), (1, 3), (3, 1), (3, 3)]
        )


class MiddleGameTestCase(unittest.TestCase):
    def test_xoeeeeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('xo'), 'x').positions,
            [(2, 1), (2, 2), (3, 1)]
        )

    def test_xeoeeeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('x.o'), 'x').positions,
            [(2, 1), (3, 1), (3, 3)]
        )

    def test_xeeeoeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('x...o'), 'x').positions,
            [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]
        )

    def test_xeeeeoeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('x....o'), 'x').positions,
            [(1, 3), (2, 2), (3, 1)]
        )

    def test_xeeeeeeeo(self):
        self.assertEqual(ai.evaluate(Board.fromstring('x.......o'), 'x').positions,
            [(1, 3), (3, 1)]
        )


class EndGameTestCase(unittest.TestCase):
    def test_xoexoeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('xo.xo.'), 'x').positions,
            [(3, 1)]
        )

    def test_xoexoeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('xo.xo.'), 'o').positions,
            [(3, 2)]
        )

    def test_xexeoeeee(self):
        self.assertEqual(ai.evaluate(Board.fromstring('x.x.o'), 'o').positions,
            [(1, 2)]
        )

    def test_xeooeexex(self):
        self.assertEqual(ai.evaluate(Board.fromstring('x.oo..x.x'), 'o').positions,
            [(1, 2), (2, 2), (2, 3), (3, 2)]
        )


class BadArgumentTestCase(unittest.TestCase):
    def test_when_not_a_token(self):
        with self.assertRaisesRegex(ValueError, 'must be a token: .'):
            ai.evaluate(Board.fromstring(), '.')

    def test_when_no_moves_available(self):
        with self.assertRaisesRegex(ValueError, 'no available moves: xxxoo....'):
            ai.evaluate(Board.fromstring('xxxoo'), 'x')

        with self.assertRaisesRegex(ValueError, 'no available moves: xxxoo....'):
            ai.evaluate(Board.fromstring('xxxoo'), 'o')

    def test_when_board_is_invalid(self):
        with self.assertRaisesRegex(ValueError, 'invalid board: xxx......'):
            ai.evaluate(Board.fromstring('xxx'), 'x')

        with self.assertRaisesRegex(ValueError, 'invalid board: xxx......'):
            ai.evaluate(Board.fromstring('xxx'), 'o')

    def test_when_not_token_turn(self):
        with self.assertRaisesRegex(ValueError, "not x's turn to play: xxo......"):
            ai.evaluate(Board.fromstring('xxo'), 'x')
