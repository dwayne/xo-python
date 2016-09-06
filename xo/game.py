from . import arbiter
from .error import IllegalStateError
from .board import isempty, isplayer, other_player, Board


STATE_INIT     = 'init'
STATE_PLAYING  = 'playing'
STATE_GAMEOVER = 'gameover'


EVENT_NAME_INVALID_MOVE = 'invalid-move'
EVENT_NAME_NEXT_TURN    = 'next-turn'
EVENT_NAME_GAMEOVER     = 'gameover'


EVENT_REASON_OUT_OF_BOUNDS = 'out-of-bounds'
EVENT_REASON_OCCUPIED      = 'occupied'
EVENT_REASON_WINNER        = 'winner'
EVENT_REASON_SQUASHED      = 'squashed'


class Game:
    def __init__(self):
        self.state = STATE_INIT
        self.board = None
        self.turn = None
        self.statistics = { 'total': 0, 'xwins': 0, 'owins': 0, 'squashed': 0 }

    def next_turn(self):
        if self.turn:
            return other_player(self.turn)
        else:
            return None

    def start(self, player):
        if self.state == STATE_INIT:
            if not isplayer(player):
                raise ValueError('expected a player: {}'.format(player))

            self.state = STATE_PLAYING
            self.board = Board.fromstring()
            self.turn = player
        else:
            raise IllegalStateError(self.state)

    def moveto(self, r, c):
        if self.state == STATE_PLAYING:
            if Board.contains(r, c):
                if isempty(self.board[r, c]):
                    self.board[r, c] = self.turn
                    last_move = { 'r': r, 'c': c, 'player': self.turn }

                    outcome = arbiter.outcome(self.board, self.turn)

                    if outcome['status'] == arbiter.STATUS_IN_PROGRESS:
                        self.turn = other_player(self.turn)

                        return {
                            'name': EVENT_NAME_NEXT_TURN,
                            'last_move': last_move
                        }
                    elif outcome['status'] == arbiter.STATUS_GAMEOVER:
                        self.state = STATE_GAMEOVER
                        self.statistics['total'] += 1

                        if outcome['reason'] == arbiter.REASON_WINNER:
                            self.statistics['{}wins'.format(self.turn)] += 1

                            return {
                                'name': EVENT_NAME_GAMEOVER,
                                'reason': EVENT_REASON_WINNER,
                                'last_move': last_move,
                                'details': outcome['details']
                            }
                        elif outcome['reason'] == arbiter.REASON_SQUASHED:
                            self.turn = other_player(self.turn)
                            self.statistics['squashed'] += 1

                            return {
                                'name': EVENT_NAME_GAMEOVER,
                                'reason': EVENT_REASON_SQUASHED,
                                'last_move': last_move
                            }
                else:
                    return {
                        'name': EVENT_NAME_INVALID_MOVE,
                        'reason': EVENT_REASON_OCCUPIED
                    }
            else:
                return {
                    'name': EVENT_NAME_INVALID_MOVE,
                    'reason': EVENT_REASON_OUT_OF_BOUNDS
                }
        else:
            raise IllegalStateError(self.state)

    def restart(self):
        if self.state == STATE_GAMEOVER:
            self.state = STATE_PLAYING
            self.board = Board.fromstring()
        else:
            raise IllegalStateError(self.state)
