from typing import Any


class ParserBase:
    """Base class for a parser, an iterator that yield all elements of a certain
    type within a given page"""
    def __init__(self, soup: 'PageElement') -> None:
        pass

    def __iter__(self) -> Any:
        raise NotImplementedError()

    def __repr__(self):
        return "<{} id={}>".format(self.__class__.__qualname__, id(self))
