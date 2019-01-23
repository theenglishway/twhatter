import logging
from typing import List

logger = logging.getLogger(__name__)

class StrategyBase:
    """Base class for strategies, which define a way to explore Tweeter pages"""
    starting_node = None
    parser_classes = []

    def __init__(self, starting_node: 'NodeBase', *parser_classes: 'ParserBase') -> None:
        """
        :param starting_node: the node from which exploration starts
        :param parser_classes: parsers that should be applied on each iteration
        of the node
        """
        self.starting_node = starting_node
        self.parser_classes = parser_classes

    def __call__(self, output) -> None:
        logger.debug("Applying {}".format(self))

    def __repr__(self):
        return "<{} (starting_node={}, parsers={})>".format(
            self.__class__.__qualname__,
            self.starting_node,
            self.parser_classes
        )
