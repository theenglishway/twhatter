from typing import Any


class ParserBase:
    """Base class for a parser
    A parser behaves like a generators, and yield all elements of a certain
    type within the original page"""
    def __init__(self, soup: 'PageElement') -> None:
        raise NotImplementedError()

    def __iter__(self) -> Any:
        raise NotImplementedError()

    def __repr__(self):
        return "<{} id={}>".format(self.__class__.__qualname__, id(self))
