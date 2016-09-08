import unittest

import xo.game as game

from xo.error import IllegalStateError
from xo.game import Game


class InitStateTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_it_is_in_init_state(self):
        self.assertEqual(self.game.state, game.STATE_INIT)
        self.assertIsNone(self.game.board)
        self.assertIsNone(self.game.turn)
        self.assertIsNone(self.game.next_turn())

    def test_it_is_not_allowed_to_call_moveto(self):
        with self.assertRaisesRegex(IllegalStateError, game.STATE_INIT):
            self.game.moveto(1, 1)

    def test_it_is_not_allowed_to_call_restart(self):
        with self.assertRaisesRegex(IllegalStateError, game.STATE_INIT):
            self.game.restart()


class PlayingStateTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start('x')

    def test_it_is_in_playing_state(self):
        self.assertEqual(self.game.state, game.STATE_PLAYING)
        self.assertEqual(str(self.game.board), '.........')
        self.assertEqual(self.game.turn, 'x')
        self.assertEqual(self.game.next_turn(), 'o')

    def test_it_is_not_allowed_to_call_start(self):
        with self.assertRaisesRegex(IllegalStateError, game.STATE_PLAYING):
            self.game.start('o')

    def test_it_is_not_allowed_to_call_restart(self):
        with self.assertRaisesRegex(IllegalStateError, game.STATE_PLAYING):
            self.game.restart()


class GameoverStateTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start('o')
        self.game.moveto(1, 1)
        self.game.moveto(1, 2)
        self.game.moveto(2, 1)
        self.game.moveto(2, 2)
        self.game.moveto(3, 1)

    def test_it_is_in_gameover_state(self):
        self.assertEqual(self.game.state, game.STATE_GAMEOVER)
        self.assertEqual(str(self.game.board), 'ox.ox.o..')
        self.assertEqual(self.game.turn, 'o')
        self.assertEqual(self.game.next_turn(), 'x')
        self.assertEqual(self.game.statistics['total'], 1)
        self.assertEqual(self.game.statistics['xwins'], 0)
        self.assertEqual(self.game.statistics['owins'], 1)
        self.assertEqual(self.game.statistics['squashed'], 0)

    def test_it_is_not_allowed_to_call_start(self):
        with self.assertRaisesRegex(IllegalStateError, game.STATE_GAMEOVER):
            self.game.start('x')

    def test_it_is_not_allowed_to_call_moveto(self):
        with self.assertRaisesRegex(IllegalStateError, game.STATE_GAMEOVER):
            self.game.moveto(2, 2)


class GamePlayTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start('x')

    def test_when_move_is_out_of_bounds(self):
        event = self.game.moveto(0, 1)

        self.assertEqual(event['name'], game.EVENT_NAME_INVALID_MOVE)
        self.assertEqual(event['reason'], game.EVENT_REASON_OUT_OF_BOUNDS)

    def test_when_move_is_to_an_occupied_position(self):
        self.game.moveto(1, 1)
        event = self.game.moveto(1, 1)

        self.assertEqual(event['name'], game.EVENT_NAME_INVALID_MOVE)
        self.assertEqual(event['reason'], game.EVENT_REASON_OCCUPIED)

    def test_when_next_turn(self):
        event = self.game.moveto(1, 1)

        self.assertEqual(event['name'], game.EVENT_NAME_NEXT_TURN)
        self.assertEqual(
            event['last_move'],
            { 'r': 1, 'c': 1, 'token': 'x' }
        )

        self.assertEqual(self.game.state, game.STATE_PLAYING)
        self.assertEqual(str(self.game.board), 'x........')
        self.assertEqual(self.game.turn, 'o')
        self.assertEqual(self.game.next_turn(), 'x')

    def test_when_x_wins(self):
        self.game.moveto(2, 2)
        self.game.moveto(1, 2)
        self.game.moveto(2, 1)
        self.game.moveto(2, 3)
        self.game.moveto(1, 1)
        self.game.moveto(3, 1)
        event = self.game.moveto(3, 3)

        self.assertEqual(event['name'], game.EVENT_NAME_GAMEOVER)
        self.assertEqual(
            event['last_move'],
            { 'r': 3, 'c': 3, 'token': 'x' }
        )
        self.assertEqual(
            event['details'],
            [{
                'index': 1,
                'where': 'diagonal',
                'positions': [(1, 1), (2, 2), (3, 3)]
            }]
        )

        self.assertEqual(self.game.state, game.STATE_GAMEOVER)
        self.assertEqual(str(self.game.board), 'xo.xxoo.x')
        self.assertEqual(self.game.turn, 'x')
        self.assertEqual(self.game.next_turn(), 'o')
        self.assertEqual(self.game.statistics['total'], 1)
        self.assertEqual(self.game.statistics['xwins'], 1)
        self.assertEqual(self.game.statistics['owins'], 0)
        self.assertEqual(self.game.statistics['squashed'], 0)

    def test_when_game_is_squashed(self):
        self.game.moveto(1, 1)
        self.game.moveto(2, 2)
        self.game.moveto(3, 3)
        self.game.moveto(2, 3)
        self.game.moveto(2, 1)
        self.game.moveto(3, 1)
        self.game.moveto(1, 3)
        self.game.moveto(1, 2)
        event = self.game.moveto(3, 2)

        self.assertEqual(event['name'], game.EVENT_NAME_GAMEOVER)
        self.assertEqual(event['reason'], game.EVENT_REASON_SQUASHED)
        self.assertEqual(
            event['last_move'],
            { 'r': 3, 'c': 2, 'token': 'x' }
        )

        self.assertEqual(self.game.state, game.STATE_GAMEOVER)
        self.assertEqual(str(self.game.board), 'xoxxoooxx')
        self.assertEqual(self.game.turn, 'x')
        self.assertEqual(self.game.next_turn(), 'o')
        self.assertEqual(self.game.statistics['total'], 1)
        self.assertEqual(self.game.statistics['xwins'], 0)
        self.assertEqual(self.game.statistics['owins'], 0)
        self.assertEqual(self.game.statistics['squashed'], 1)


class RestartGameTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start('o')

    def test_restart_after_a_win(self):
        self.game.moveto(1, 3)
        self.game.moveto(1, 1)
        self.game.moveto(2, 3)
        self.game.moveto(2, 1)
        self.game.moveto(3, 3)

        self.game.restart()

        self.assertEqual(self.game.state, game.STATE_PLAYING)
        self.assertEqual(str(self.game.board), '.........')
        self.assertEqual(self.game.turn, 'o')
        self.assertEqual(self.game.next_turn(), 'x')
        self.assertEqual(self.game.statistics['total'], 1)
        self.assertEqual(self.game.statistics['xwins'], 0)
        self.assertEqual(self.game.statistics['owins'], 1)
        self.assertEqual(self.game.statistics['squashed'], 0)

    def test_restart_after_a_squashed_game(self):
        self.game.moveto(1, 1)
        self.game.moveto(2, 2)
        self.game.moveto(3, 3)
        self.game.moveto(2, 3)
        self.game.moveto(2, 1)
        self.game.moveto(3, 1)
        self.game.moveto(1, 3)
        self.game.moveto(1, 2)
        self.game.moveto(3, 2)

        self.game.restart()

        self.assertEqual(self.game.state, game.STATE_PLAYING)
        self.assertEqual(str(self.game.board), '.........')
        self.assertEqual(self.game.turn, 'x')
        self.assertEqual(self.game.next_turn(), 'o')
        self.assertEqual(self.game.statistics['total'], 1)
        self.assertEqual(self.game.statistics['xwins'], 0)
        self.assertEqual(self.game.statistics['owins'], 0)
        self.assertEqual(self.game.statistics['squashed'], 1)
