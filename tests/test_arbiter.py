import unittest

import xo.arbiter as arbiter
from xo.board import Board


class InProgressPositionsTestCase(unittest.TestCase):
    def test_when_board_is_empty(self):
        self.assertEqual(
            arbiter.outcome(Board.fromstring(), 'x')['status'],
            arbiter.STATUS_IN_PROGRESS
        )

        self.assertEqual(
            arbiter.outcome(Board.fromstring(), 'o')['status'],
            arbiter.STATUS_IN_PROGRESS
        )

    def test_when_board_is_exeoex(self):
        self.assertEqual(
            arbiter.outcome(Board.fromstring(' x o x'), 'x')['status'],
            arbiter.STATUS_IN_PROGRESS
        )

        self.assertEqual(
            arbiter.outcome(Board.fromstring(' x o x'), 'o')['status'],
            arbiter.STATUS_IN_PROGRESS
        )


class GameoverPositionsTestCase(unittest.TestCase):
    def test_when_x_wins(self):
        outcome = arbiter.outcome(Board.fromstring('xxxoo'), 'x')

        self.assertEqual(outcome['status'], arbiter.STATUS_GAMEOVER)
        self.assertEqual(outcome['reason'], arbiter.REASON_WINNER)
        self.assertEqual(outcome['details'], [{
            'where': 'row',
            'index': 1,
            'positions': [(1, 1), (1, 2), (1, 3)]
        }])

    def test_when_o_loses(self):
        outcome = arbiter.outcome(Board.fromstring('oo xxx'), 'o')

        self.assertEqual(outcome['status'], arbiter.STATUS_GAMEOVER)
        self.assertEqual(outcome['reason'], arbiter.REASON_LOSER)
        self.assertEqual(outcome['details'], [{
            'where': 'row',
            'index': 2,
            'positions': [(2, 1), (2, 2), (2, 3)]
        }])

    def test_when_game_is_squashed(self):
        for player in ['x', 'o']:
            outcome = arbiter.outcome(Board.fromstring('xoxxoooxx'), player)

            self.assertEqual(outcome['status'], arbiter.STATUS_GAMEOVER)
            self.assertEqual(outcome['reason'], arbiter.REASON_SQUASHED)


class InvalidPositionsTestCase(unittest.TestCase):
    def test_when_too_many_moves_ahead(self):
        for player in ['x', 'o']:
            outcome = arbiter.outcome(Board.fromstring('xx'), player)

            self.assertEqual(outcome['status'], arbiter.STATUS_INVALID)
            self.assertEqual(
                outcome['reason'],
                arbiter.REASON_TOO_MANY_MOVES_AHEAD
            )

    def test_when_two_winners(self):
        for player in ['x', 'o']:
            outcome = arbiter.outcome(Board.fromstring('xo xo xo'), player)

            self.assertEqual(outcome['status'], arbiter.STATUS_INVALID)
            self.assertEqual(outcome['reason'], arbiter.REASON_TWO_WINNERS)


class ArgumentErrorTestCase(unittest.TestCase):
    def test_when_not_given_a_player(self):
        with self.assertRaisesRegex(ValueError, 'expected a player:  '):
            arbiter.outcome(Board.fromstring(), ' ')


class CountPiecesTestCase(unittest.TestCase):
    def test_it_computes_the_number_of_xs_os_and_es(self):
        piece_counts = arbiter.count_pieces(Board.fromstring('xoxoo'))

        self.assertEqual(piece_counts['xs'], 2)
        self.assertEqual(piece_counts['os'], 3)
        self.assertEqual(piece_counts['es'], 4)
