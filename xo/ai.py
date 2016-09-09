import math

from collections import namedtuple

from . import arbiter
from .board import ncells
from .token import isempty, istoken, other_token


MinimaxResult = namedtuple('MinimaxResult', 'score depth positions')


def evaluate(board, token, use_cache=True):
    outcome = arbiter.outcome(board, token)

    if outcome['status'] == arbiter.STATUS_IN_PROGRESS:
        other = other_token(token)
        token_piece_count = outcome['piece_counts']['{}s'.format(token)]
        other_piece_count = outcome['piece_counts']['{}s'.format(other)]

        if token_piece_count <= other_piece_count:
            if use_cache and outcome['piece_counts']['es'] >= ncells - 1:
                return _cached_minimax_result[str(board)]
            else:
                return _maximize(board, token, other, 0)
        else:
            raise ValueError("not {}'s turn to play: {}".format(token, board))
    elif outcome['status'] == arbiter.STATUS_GAMEOVER:
        raise ValueError('no available moves: {}'.format(board))
    else:
        raise ValueError('invalid board: {}'.format(board))


def _maximize(board, a, b, depth):
    outcome = arbiter.outcome(board, b)

    if _terminal(outcome):
        return MinimaxResult(_min_terminal_score(outcome, depth), depth, [])

    max_score = -math.inf
    max_positions = []

    for r, c, piece in board:
        if isempty(piece):
            pos = (r, c)

            board[pos] = a

            min_score, min_depth, _ = _minimize(board, b, a, depth + 1)

            if min_score > max_score:
                max_score = min_score
                max_depth = min_depth
                max_positions = [pos]
            elif min_score == max_score:
                max_depth = min_depth
                max_positions.append(pos)

            board[pos] = ' '

    return MinimaxResult(max_score, max_depth, max_positions)


def _minimize(board, a, b, depth):
    outcome = arbiter.outcome(board, b)

    if _terminal(outcome):
        return MinimaxResult(_max_terminal_score(outcome, depth), depth, [])

    min_score = math.inf
    min_positions = []

    for r, c, piece in board:
        if isempty(piece):
            pos = (r, c)

            board[pos] = a

            max_score, max_depth, _ = _maximize(board, b, a, depth + 1)

            if max_score < min_score:
                min_score = max_score
                min_depth = max_depth
                min_positions = [pos]
            elif max_score == min_score:
                min_depth = max_depth
                min_positions.append(pos)

            board[pos] = ' '

    return MinimaxResult(min_score, min_depth, min_positions)


def _terminal(outcome):
    return outcome['status'] == arbiter.STATUS_GAMEOVER


_maximum_depth = 9


def _max_terminal_score(outcome, depth):
    if outcome['reason'] == arbiter.REASON_WINNER:
        return 2 * (_maximum_depth - depth) + _maximum_depth + 1
    elif outcome['reason'] == arbiter.REASON_SQUASHED:
        return depth
    else:
        # Should never be reached
        raise ValueError('unexpected outcome: {}'.format(outcome))


def _min_terminal_score(outcome, depth):
    return -_max_terminal_score(outcome, depth)


_cached_minimax_result = {
    '.........': MinimaxResult(score=9, depth=9, positions=[
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3)
    ]),
    'x........': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ]),
    '.x.......': MinimaxResult(score=-8, depth=8, positions=[
        (1, 1), (1, 3),
        (2, 2), (3, 2)
    ]),
    '..x......': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ]),
    '...x.....': MinimaxResult(score=-8, depth=8, positions=[
        (1, 1), (2, 2),
        (2, 3), (3, 1)
    ]),
    '....x....': MinimaxResult(score=-8, depth=8, positions=[
        (1, 1), (1, 3),
        (3, 1), (3, 3)
    ]),
    '.....x...': MinimaxResult(score=-8, depth=8, positions=[
        (1, 3), (2, 1),
        (2, 2), (3, 3)
    ]),
    '......x..': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ]),
    '.......x.': MinimaxResult(score=-8, depth=8, positions=[
        (1, 2), (2, 2),
        (3, 1), (3, 3)
    ]),
    '........x': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ]),
    'o........': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ]),
    '.o.......': MinimaxResult(score=-8, depth=8, positions=[
        (1, 1), (1, 3),
        (2, 2), (3, 2)
    ]),
    '..o......': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ]),
    '...o.....': MinimaxResult(score=-8, depth=8, positions=[
        (1, 1), (2, 2),
        (2, 3), (3, 1)
    ]),
    '....o....': MinimaxResult(score=-8, depth=8, positions=[
        (1, 1), (1, 3),
        (3, 1), (3, 3)
    ]),
    '.....o...': MinimaxResult(score=-8, depth=8, positions=[
        (1, 3), (2, 1),
        (2, 2), (3, 3)
    ]),
    '......o..': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ]),
    '.......o.': MinimaxResult(score=-8, depth=8, positions=[
        (1, 2), (2, 2),
        (3, 1), (3, 3)
    ]),
    '........o': MinimaxResult(score=-8, depth=8, positions=[
        (2, 2)
    ])
}
