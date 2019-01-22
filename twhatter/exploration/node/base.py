import logging

logger = logging.getLogger(__name__)

class NodeBase:
    """Base class for nodes, which are all the pages that Twitter allows us
    to visit. They can be iterated on, and will yield 'soup' within the limits
    defined at initialization"""
    def __init__(self):
        logger.debug("Initializing {}".format(self.__class__.__qualname__))

    def __iter__(self) -> 'PageElement':
        logger.debug("Iterating on {}".format(self.__class__.__qualname__))
