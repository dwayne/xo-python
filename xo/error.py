"""Exception classes raised by xo.

The base exception class is XOError, which inherits from Exception. It doesn't
define any behavior of its own, but is the base class for all exceptions defined
in this package.
"""


class XOError(Exception):
    pass


class IllegalStateError(XOError):
    pass
