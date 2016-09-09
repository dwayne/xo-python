xo
==

.. image:: https://img.shields.io/pypi/v/xo.svg
    :target: https://pypi.python.org/pypi/xo

A `Python <https://www.python.org/>`_ CLI game and library for `Tic-tac-toe <http://en.wikipedia.org/wiki/Tic-tac-toe>`_.

The library is written in a modular way. Its overall design consists of 4 decoupled components:

1. A Tic-tac-toe board data structure, ``xo.board``.
2. An arbiter for analyzing the state of a board, ``xo.arbiter``.
3. A game engine to implement and enforce the Tic-tac-toe game logic, ``xo.game``.
4. And finally, an AI for finding excellent moves, ``xo.ai``.

**The board**

.. code-block:: python

    >>> from xo.board import isempty, Board

    >>> board = Board.fromstring('..x.o')
    >>> print(board)
    ..x.o....

    >>> print(board.toascii())
       |   | x
    ---+---+---
       | o |
    ---+---+---
       |   |

    >>> board[1, 3]
    x
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

The board isn't concerned with whether or not a given layout can be reached in an actual Tic-tac-toe game. Hence, the following is perfectly legal:

.. code-block:: python

    >>> board = Board.fromstring('xxxxxxxxo')
    >>> print(board)
    xxxxxxxxo

The arbiter is concerned about that though and can detect such invalid board layouts.

**The arbiter**

.. code-block:: python

    >>> from xo import arbiter
    >>> from xo.board import Board

    >>> arbiter.outcome(Board.fromstring(), 'x')
    {
      'piece_counts': {'os': 0, 'xs': 0, 'es': 9},
      'status': 'in-progress'
    }

    >>> arbiter.outcome(Board.fromstring('xxxoo'), 'o')
    {
      'piece_counts': {'os': 2, 'xs': 3, 'es': 4},
      'details': [
        {'index': 1, 'positions': [(1, 1), (1, 2), (1, 3)], 'where': 'row'}
      ],
      'status': 'gameover',
      'reason': 'loser'
    }

    >>> arbiter.outcome(Board.fromstring('xxxxxxxxo'), 'x')
    {
      'piece_counts': {'os': 1, 'xs': 8, 'es': 0},
      'status': 'invalid',
      'reason': 'too-many-moves-ahead'
    }

**The game engine**

Enforcer of the game rules.

.. code-block:: python

    >>> from xo.game import Game

    >>> game = Game()
    >>> game.start('x')
    >>> game.moveto(1, 1)
    {
      'name': 'next-turn',
      'last_move': {'token': 'x', 'r': 1, 'c': 1}
    }
    >>> game.moveto(1, 1)
    {
      'name': 'invalid-move',
      'reason': 'occupied'
    }
    >>> game.moveto(0, 0)
    {
      'name': 'invalid-move',
      'reason': 'out-of-bounds'
    }
    >>> game.moveto(2, 2)
    {
      'name': 'next-turn',
      'last_move': {'token': 'o', 'r': 2, 'c': 2}
    }
    >>> game.moveto(3, 1)
    {
      'name': 'next-turn',
      'last_move': {'token': 'x', 'r': 3, 'c': 1}
    }
    >>> print(game.board.toascii())
     x |   |
    ---+---+---
       | o |
    ---+---+---
     x |   |

    >>> game.moveto(3, 3)
    {
      'name': 'next-turn',
      'last_move': {'token': 'o', 'r': 3, 'c': 3}
    }
    >>> game.moveto(2, 1)
    {
      'name': 'gameover',
      'reason': 'winner',
      'last_move': {'token': 'x', 'r': 2, 'c': 1},
      'details': [{'index': 1, 'positions': [(1, 1), (2, 1), (3, 1)], 'where': 'column'}]
    }

    >>> game.moveto(1, 3)
    ...
    xo.error.IllegalStateError: gameover

    >>> # start a new game
    >>> game.restart()
    >>> # since x won, it would be x's turn to play
    >>> # if the game was squashed then it would have been o's turn to play
    >>> game.moveto(1, 1)
    >>> print(game.board.toascii())
     x |   |
    ---+---+---
       |   |
    ---+---+---
       |   |

**The AI**

No Tic-tac-toe library is complete without an AI that can play a perfect game of Tic-tac-toe.

.. code-block:: python

    >>> from xo import ai
    >>> from xo.board import Board

    >>> ai.evaluate(Board.fromstring('xo.xo.'), 'x')
    MinimaxResult(score=26, depth=1, positions=[(3, 1)])

    >>> ai.evaluate(Board.fromstring('xo.xo.'), 'o')
    MinimaxResult(score=26, depth=1, positions=[(3, 2)])

    >>> ai.evaluate(Board.fromstring('x.o'), 'x')
    MinimaxResult(score=18, depth=5, positions=[(2, 1), (3, 1), (3, 3)])

Finally, ``xo.cli`` brings it all together in its implementation of the command-line Tic-tac-toe game. It's interesting to see how easy it becomes to implement the game so be sure to check it out.

**Note:** *An extensive suite of tests is also available that can help you better understand how each component is supposed to work.*

Installation
------------

Install it using:

.. code-block:: bash

    $ pip install xo

You would now have access to an executable called ``xo``. Type

.. code-block:: bash

    $ xo

to starting playing immediately.

Usage
-----

For help, type

.. code-block:: bash

    $ xo -h

By default ``xo`` is configured for a human player to play with ``x`` and a computer player to play with ``o``. However, this can be easily changed to allow any of the other 3 possibilities:

.. code-block:: bash

    $ # Computer vs Human
    $ xo -x computer -o human

    $ # Human vs Human
    $ xo -x human -o human
    $ xo -o human # since x defaults to human

    $ # Computer vs Computer
    $ xo -x computer -o computer
    $ xo -x computer # since o defaults to computer

You can also change who plays first. By default it's the ``x`` player.

.. code-block:: bash

    $ # Let o play first
    $ xo -f o

Finally, when letting the computers battle it out you can specify the number of times you want them to play each other. By default they play 50 rounds.

.. code-block:: bash

    $ xo -x computer -r 5
    .....

    Game statistics
    ---------------
    Total games played: 5 (2.438 secs)
    Number of times x won: 0
    Number of times o won: 0
    Number of squashed games: 5

Development
-----------

Get the source code.

.. code-block:: bash

    $ git clone git@github.com:dwayne/xo-python.git

Create a `virtual environment <https://docs.python.org/3/library/venv.html>`_ and activate it.

.. code-block:: bash

    $ cd xo-python
    $ pyvenv venv
    $ . venv/bin/activate

Then, upgrade ``pip`` and ``setuptools`` and install the development dependencies.

.. code-block:: bash

    (venv) $ pip install -U pip setuptools
    (venv) $ pip install -r requirements-dev.txt

You're now all set to begin development.

Testing
-------

Tests are written using the `unittest <https://docs.python.org/3/library/unittest.html>`_ unit testing framework.

Run all tests.

.. code-block:: bash

    (venv) $ python -m unittest

Run a specific test module.

.. code-block:: bash

    (venv) $ python -m unittest tests.test_arbiter

Run a specific test case.

.. code-block:: bash

    (venv) $ python -m unittest tests.test_arbiter.GameoverPositionsTestCase

Run a specific test method.

.. code-block:: bash

    (venv) $ python -m unittest tests.test_arbiter.GameoverPositionsTestCase.test_when_x_wins

Credits
-------

Thanks to `Patrick Henry Winston <http://people.csail.mit.edu/phw/>`_ for clarifying the Minimax algorithm. His `video <https://www.youtube.com/watch?v=STjW3eH0Cik>`_ on the topic was a joy to watch.

Copyright
---------

Copyright (c) 2016 Dwayne Crooks. See `LICENSE </LICENSE.txt>`_ for further details.
