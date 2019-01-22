import logging
from typing import List

logger = logging.getLogger(__name__)

class StrategyBase:
    """Base class for strategies, which define a way to explore Tweeter pages"""
    starting_node = None
    parser_classes = []

    def __init__(self, starting_node: 'NodeBase', *parser_classes: 'ParserBase') -> None:
        logger.debug(
            "Initializing {} with starting_node={} and parser_classes={}".format(
                self.__class__.__qualname__,
                starting_node,
                parser_classes
            )
        )
        self.starting_node = starting_node
        self.parser_classes = parser_classes

    def __call__(self, output) -> None:
        logger.debug("Applying {}".format(self.__class__.__qualname__))

    def __repr__(self):
        return "<{} (starting_node={}, parsers={})>".format(
            self.__class__.__qualname__,
            self.starting_node,
            self.parser_classes
        )
