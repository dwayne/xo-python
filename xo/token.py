""" A token is either 'x' or 'o'. Anything else is considered an empty piece.

The tokens together with all the different representations of the empty piece
are all called pieces.

The canonical pieces are just 'x', 'o' and ' '.
"""


def istoken(c):
    return c == 'x' or c == 'o'

def isempty(c):
    return not istoken(c)

def other_token(t):
    if t == 'x':
        return 'o'
    elif t == 'o':
        return 'x'
    else:
        raise ValueError('must be a token: {}'.format(t))

def canonical_piece(c):
    if c == 'x' or c == 'o':
        return c
    return ' '
