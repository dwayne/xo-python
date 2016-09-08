import random
import re
import sys
import time

from collections import namedtuple

from . import ai, game
from .token import isempty, istoken, other_token


Player = namedtuple('Player', 'token ishuman')


class Console:
    def __init__(self, input=sys.stdin, output=sys.stdout):
        self.input = input
        self.output = output

    def write(self, s):
        self.output.write(s)
        self.output.flush()

    def writeln(self, s=''):
        self.write(s + '\n')

    def getln(self, prompt='> '):
        self.write(prompt)
        return self.input.readline()


class Orchestrator:
    def __init__(self, player1=Player('x', True), player2=Player('o', False), console=Console()):
        if not istoken(player1.token):
            raise ValueError('player1 has an invalid token: {}'.format(player1.token))
        if not istoken(player2.token):
            raise ValueError('player2 has an invalid token: {}'.format(player2.token))
        if player1.token == player2.token:
            raise ValueError('both players cannot play with the same token: {}'.format(player1.token))

        self._first_player = player1

        self._players = {}
        self._players[player1.token] = player1
        self._players[player2.token] = player2

        self._console = console

        self._num_human_players = 0
        if player1.ishuman:
            self._num_human_players += 1
        if player2.ishuman:
            self._num_human_players += 1

    def start(self, rounds=50):
        start_time = time.time()

        try:
            self._play(rounds)
        except KeyboardInterrupt:
            self._console.writeln()
            if self._num_human_players > 0:
                self._console.writeln("We're deeply saddened to see you go, ;(.")

        self._elapsed_time = time.time() - start_time
        self._show_game_statistics()

        if self._num_human_players > 0:
            self._console.writeln()
            self._console.writeln('Thank you for playing. Please come back anytime.')

    def _play(self, rounds):
        self._init_and_start_game()

        if self._num_human_players == 0:
            playing = rounds > 0
        else:
            self._console.writeln('Welcome to Tic-tac-toe')
            self._console.writeln('Play as many games as you want')
            self._console.writeln('Press Ctrl-C to exit at any time')
            self._console.writeln()
            playing = True

        while playing:
            event = self._play_one_turn()

            if event['name'] == game.EVENT_NAME_GAMEOVER:
                self._handle_game_over(event['reason'])

                if self._num_human_players == 0:
                    rounds -= 1
                    playing = rounds > 0

                    if not playing:
                        self._console.writeln()
                else:
                    playing = self._ask_to_play_again(event)

                if playing:
                    self._game.restart()

    def _init_and_start_game(self):
        self._game = game.Game()
        self._game.start(self._first_player.token)

    def _play_one_turn(self):
        player = self._current_player()

        if player.ishuman:
            if self._num_human_players == 2:
                self._console.writeln("{}'s turn".format(player.token))
            else:
                self._console.writeln('Your turn ({})'.format(player.token))

            self._console.writeln(self._game.board.toascii())

            while True:
                r, c = self._get_input_move()
                event = self._game.moveto(r, c)

                if event['name'] == game.EVENT_NAME_INVALID_MOVE:
                    if event['reason'] == game.EVENT_REASON_OUT_OF_BOUNDS:
                        self._console.writeln('Sorry, but that move was not on the board')
                    elif event['reason'] == game.EVENT_REASON_OCCUPIED:
                        self._console.writeln('Sorry, but that position is already taken')
                    self._console.writeln('Please, try again')
                else:
                    return event
        else:
            positions = ai.evaluate(self._game.board, self._game.turn).positions
            random.shuffle(positions)
            r, c = positions[0]
            event = self._game.moveto(r, c)

            if self._num_human_players == 1:
                self._console.writeln('The computer played at {}, {}'.format(r, c))

            return event

    def _handle_game_over(self, reason):
        player = self._current_player()

        if reason == game.EVENT_REASON_WINNER:
            if self._num_human_players == 2:
                self._console.writeln('Congratulations! {} won.'.format(player.token))
            elif self._num_human_players == 1:
                if player.ishuman:
                    self._console.writeln('Congratulations! You won.')
                else:
                    self._console.writeln('The computer won. Better luck next time.')
            else:
                self._console.write(player.token)
        elif reason == game.EVENT_REASON_SQUASHED:
            if self._num_human_players > 0:
                self._console.writeln('Game squashed.')
            else:
                self._console.write('.')

        if self._num_human_players > 0:
            self._console.writeln(self._game.board.toascii())

    def _get_input_move(self):
        show_help = True

        while True:
            s = self._console.getln()
            s = re.split('\s+', s.strip())
            if len(s) == 2:
                try:
                    return [int(t) for t in s]
                except ValueError:
                    pass

            if show_help:
                show_help = False
                self._console.writeln('Please enter a move in the format "r c", where r and c are numbers for e.g.')
                r, c = self._first_open_position()
                self._console.writeln('> {} {}'.format(r, c))

    def _first_open_position(self):
        for r, c, piece in self._game.board:
            if isempty(piece):
                return r, c

    def _ask_to_play_again(self, event):
        self._console.writeln('Do you want to play again? (Y/n)')

        while True:
            s = self._console.getln()
            s = s.strip().lower()
            if s in ['', 'y', 'yes']:
                return True
            elif s in ['n', 'no']:
                return False

    def _show_game_statistics(self):
        stats = self._game.statistics

        self._console.writeln()
        self._console.writeln('Game statistics')
        self._console.writeln('---------------')
        if self._num_human_players == 0:
            self._console.writeln('Total games played: {} ({:.3f} secs)'.format(
                stats['total'], self._elapsed_time))
        else:
            self._console.writeln('Total games played: {}'.format(stats['total']))
        self._console.writeln('Number of times x won: {}'.format(stats['xwins']))
        self._console.writeln('Number of times o won: {}'.format(stats['owins']))
        self._console.writeln('Number of squashed games: {}'.format(stats['squashed']))

    def _current_player(self):
        return self._players[self._game.turn]


def main():
    import argparse

    parser = argparse.ArgumentParser(description='A Tic-tac-toe game.')

    player_choices = ['human', 'computer']

    parser.add_argument('-x', choices=player_choices, default='human',
        help='who controls x (default: human)')
    parser.add_argument('-o', choices=player_choices, default='computer',
        help='who controls o (default: computer)')

    parser.add_argument('-r', '--rounds', type=int, default=50,
        metavar='n',
        help='the number of rounds to let two computer players play (default: 50)')

    parser.add_argument('-f', '--first', choices=['x', 'o'], default='x',
        help='who plays first (default: x)')

    args = parser.parse_args()

    players = {
        'x': Player('x', args.x == 'human'),
        'o': Player('o', args.o == 'human')
    }

    player1 = players[args.first]
    player2 = players[other_token(args.first)]

    rounds = max(0, args.rounds)

    Orchestrator(player1, player2).start(rounds)

    return 0
