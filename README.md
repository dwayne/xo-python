# xo

[![Latest PyPI version](https://img.shields.io/pypi/v/xo.svg "Latest PyPI version")](https://pypi.org/project/xo/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/xo.svg "Supported Python versions")](https://pypi.org/project/xo/)

A [Tic-tac-toe](http://en.wikipedia.org/wiki/Tic-tac-toe) CLI game and library written in [Python](https://www.python.org/).

The library is written in a modular way. Its overall design consists of 4 decoupled components:

1. A Tic-tac-toe board data structure, `xo.board`.
2. An arbiter for analyzing the state of a board, `xo.arbiter`.
3. A game engine to implement and enforce the Tic-tac-toe game logic, `xo.game`.
4. And finally, an AI for finding excellent moves, `xo.ai`.

**The board**

```python
>>> from xo.board import Board
>>> from xo.token import isempty

>>> board = Board.fromstring('..x.o')
>>> print(board)
..x.o....

>>> print(board.toascii()) # doctest: +NORMALIZE_WHITESPACE
   |   | x
---+---+---
   | o |
---+---+---
   |   |

>>> board[1, 3]
'x'

>>> board[3, 3] = 'x'
>>> print(board)
..x.o...x

>>> for r, c, piece in board:
...   if isempty(piece):
...     print('{}, {}'.format(r, c))
...
1, 1
1, 2
2, 1
2, 3
3, 1
3, 2

```

The board isn't concerned with whether or not a given layout can be reached in an actual Tic-tac-toe game. Hence, the following is perfectly legal:

```python
>>> board = Board.fromstring('xxxxxxxxo')
>>> print(board)
xxxxxxxxo

```

The arbiter is concerned about that though and can detect such invalid board layouts.

**The arbiter**

```python
>>> from xo import arbiter
>>> from xo.board import Board

>>> arbiter.outcome(Board.fromstring(), 'x')
{'status': 'in-progress', 'piece_counts': {'xs': 0, 'os': 0, 'es': 9}}

>>> arbiter.outcome(Board.fromstring('xxxoo'), 'o')
{'status': 'gameover', 'reason': 'loser', 'details': [{'where': 'row', 'index': 1, 'positions': [(1, 1), (1, 2), (1, 3)]}], 'piece_counts': {'xs': 3, 'os': 2, 'es': 4}}

>>> arbiter.outcome(Board.fromstring('xxxxxxxxo'), 'x')
{'status': 'invalid', 'reason': 'too-many-moves-ahead', 'piece_counts': {'xs': 8, 'os': 1, 'es': 0}}

```

**The game engine**

Enforcer of the game rules.

```python
>>> from xo.game import Game

>>> game = Game()
>>> game.start('x')
>>> game.moveto(1, 1)
{'name': 'next-turn', 'last_move': {'r': 1, 'c': 1, 'token': 'x'}}

>>> game.moveto(1, 1)
{'name': 'invalid-move', 'reason': 'occupied'}

>>> game.moveto(0, 0)
{'name': 'invalid-move', 'reason': 'out-of-bounds'}

>>> game.moveto(2, 2)
{'name': 'next-turn', 'last_move': {'r': 2, 'c': 2, 'token': 'o'}}

>>> game.moveto(3, 1)
{'name': 'next-turn', 'last_move': {'r': 3, 'c': 1, 'token': 'x'}}

>>> print(game.board.toascii()) # doctest: +NORMALIZE_WHITESPACE
 x |   |
---+---+---
   | o |
---+---+---
 x |   |

>>> game.moveto(3, 3)
{'name': 'next-turn', 'last_move': {'r': 3, 'c': 3, 'token': 'o'}}

>>> game.moveto(2, 1)
{'name': 'gameover', 'reason': 'winner', 'last_move': {'r': 2, 'c': 1, 'token': 'x'}, 'details': [{'where': 'column', 'index': 1, 'positions': [(1, 1), (2, 1), (3, 1)]}]}

>>> game.moveto(1, 3)
Traceback (most recent call last):
...
xo.error.IllegalStateError: gameover

>>> # start a new game
>>> game.restart()
>>> # since x won, it would be x's turn to play
>>> # if the game was squashed then it would have been o's turn to play
>>> game.moveto(1, 1)
{'name': 'next-turn', 'last_move': {'r': 1, 'c': 1, 'token': 'x'}}

>>> print(game.board.toascii()) # doctest: +NORMALIZE_WHITESPACE
 x |   |
---+---+---
   |   |
---+---+---
   |   |

```

**The AI**

No Tic-tac-toe library is complete without an AI that can play a perfect game of Tic-tac-toe.

```python
>>> from xo import ai
>>> from xo.board import Board

>>> ai.evaluate(Board.fromstring('xo.xo.'), 'x')
MinimaxResult(score=26, depth=1, positions=[(3, 1)])

>>> ai.evaluate(Board.fromstring('xo.xo.'), 'o')
MinimaxResult(score=26, depth=1, positions=[(3, 2)])

>>> ai.evaluate(Board.fromstring('x.o'), 'x')
MinimaxResult(score=18, depth=5, positions=[(2, 1), (3, 1), (3, 3)])

```

Finally, `xo.cli` brings it all together in its implementation of the command-line Tic-tac-toe game. It's interesting to see how easy it becomes to implement the game so be sure to check it out.

**Note:** *An extensive suite of tests is also available that can help you better understand how each component is supposed to work.*

## Installation

Install it using pip, or your favourite Python package manager:

```bash
pip install xo
```

You would now have access to an executable called `xo`. Type

```bash
xo
```

to start playing immediately.

## Usage

For help, type

```bash
xo -h
```

By default `xo` is configured for a human player to play with `x` and a computer player to play with `o`. However, this can be easily changed to allow any of the other 3 possibilities:

```bash
# Computer vs Human
xo -x computer -o human

# Human vs Human
xo -x human -o human
xo -o human # since x defaults to human

# Computer vs Computer
xo -x computer -o computer
xo -x computer # since o defaults to computer
```

You can also change who plays first. By default it's the `x` player.

```bash
# Let o play first
xo -f o
```

Finally, when letting the computers battle it out you can specify the number of times you want them to play each other. By default they play 50 rounds.

```bash
xo -x computer -r 5
# .....
#
# Game statistics
# ---------------
# Total games played: 5 (2.438 secs)
# Number of times x won: 0
# Number of times o won: 0
# Number of squashed games: 5
```

### With Nix

If you have [Nix](https://zero-to-nix.com/start/install/) with flakes enabled, you can play without installing anything:

```bash
nix run github:dwayne/xo-python
```

Options go after `--`:

```bash
nix run github:dwayne/xo-python -- -x computer -o computer -r 5
```

To keep `xo` on your `PATH`:

```bash
nix profile add github:dwayne/xo-python
```

From a clone of the repository, `nix run` runs your local copy.


## Development

Development also uses Nix (see [With Nix](#with-nix)). Clone the repository and enter the development shell:

```bash
git clone git@github.com:dwayne/xo-python.git
cd xo-python
nix develop
```

You're now all set to begin development. Some common tasks are available through `make`:

| Command          | What it does                                                            |
| ---------------- | ----------------------------------------------------------------------- |
| `make build`     | Build the sdist and wheel into `dist/`                                  |
| `make check`     | Build the package, run the tests and doctests, and check metadata       |
| `make check-all` | Run `make check`, then the tests on the other supported Python versions |
| `make clean`     | Remove build artifacts                                                  |

## Testing

Tests are written using the [unittest](https://docs.python.org/3/library/unittest.html) unit testing framework.

Run everything with `make check`, or run tests directly:

```bash
python -m unittest
```

Run a specific test module.

```bash
python -m unittest tests.test_arbiter
```

Run a specific test case.

```bash
python -m unittest tests.test_arbiter.GameoverPositionsTestCase
```

Run a specific test method.

```bash
python -m unittest tests.test_arbiter.GameoverPositionsTestCase.test_when_x_wins
```

## Credits

Thanks to [Patrick Henry Winston](http://people.csail.mit.edu/phw/) for clarifying the Minimax algorithm. His [video](https://www.youtube.com/watch?v=STjW3eH0Cik) on the topic was a joy to watch.
