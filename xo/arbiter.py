from .token import istoken, other_token


STATUS_INVALID     = 'invalid'
STATUS_GAMEOVER    = 'gameover'
STATUS_IN_PROGRESS = 'in-progress'


REASON_TOO_MANY_MOVES_AHEAD = 'too-many-moves-ahead'
REASON_TWO_WINNERS          = 'two-winners'
REASON_WINNER               = 'winner'
REASON_LOSER                = 'loser'
REASON_SQUASHED             = 'squashed'


def outcome(board, token):
    if not istoken(token):
        raise ValueError('must be a token: {}'.format(token))

    piece_counts = count_pieces(board)

    if _two_or_more_moves_ahead(piece_counts):
        result = {
            'status': STATUS_INVALID,
            'reason': REASON_TOO_MANY_MOVES_AHEAD
        }
    else:
        winners = _find_winners(board)

        if _has_two_winners(winners):
            result = {
                'status': STATUS_INVALID,
                'reason': REASON_TWO_WINNERS
            }
        elif _is_winner(winners, token):
            result = {
                'status': STATUS_GAMEOVER,
                'reason': REASON_WINNER,
                'details': winners[token]
            }
        elif _is_winner(winners, other_token(token)):
            result = {
                'status': STATUS_GAMEOVER,
                'reason': REASON_LOSER,
                'details': winners[other_token(token)]
            }
        elif _is_squashed(piece_counts):
            result = {
                'status': STATUS_GAMEOVER,
                'reason': REASON_SQUASHED
            }
        else:
            result = { 'status': STATUS_IN_PROGRESS }

    result['piece_counts'] = piece_counts

    return result


def count_pieces(board):
    xs, os, es = 0, 0, 0

    for _, _, piece in board:
        if piece == 'x':
            xs += 1
        elif piece == 'o':
            os += 1
        else:
            es += 1

    return { 'xs': xs, 'os': os, 'es': es }


def _two_or_more_moves_ahead(piece_counts):
    return abs(piece_counts['xs'] - piece_counts['os']) >= 2


_winning_positions = [
    { 'where': 'row', 'index': 1, 'positions': [(1, 1), (1, 2), (1, 3)] },
    { 'where': 'row', 'index': 2, 'positions': [(2, 1), (2, 2), (2, 3)] },
    { 'where': 'row', 'index': 3, 'positions': [(3, 1), (3, 2), (3, 3)] },

    { 'where': 'column', 'index': 1, 'positions': [(1, 1), (2, 1), (3, 1)] },
    { 'where': 'column', 'index': 2, 'positions': [(1, 2), (2, 2), (3, 2)] },
    { 'where': 'column', 'index': 3, 'positions': [(1, 3), (2, 3), (3, 3)] },

    { 'where': 'diagonal', 'index': 1, 'positions': [(1, 1), (2, 2), (3, 3)] },
    { 'where': 'diagonal', 'index': 2, 'positions': [(1, 3), (2, 2), (3, 1)] }
]


def _find_winners(board):
    winners = { 'x': [], 'o': [] }

    for w in _winning_positions:
        x = board[w['positions'][0]]
        y = board[w['positions'][1]]
        z = board[w['positions'][2]]

        if _is_winning(x, y, z):
            winners[x].append({
                'where': w['where'],
                'index': w['index'],
                'positions': list(w['positions'])
            })

    return winners


def _is_winning(x, y, z):
    return istoken(x) and x == y and y == z


def _has_two_winners(winners):
    return len(winners['x']) > 0 and len(winners['o']) > 0


def _is_winner(winners, token):
    return len(winners[token]) > 0


def _is_squashed(piece_counts):
    return piece_counts['es'] == 0
