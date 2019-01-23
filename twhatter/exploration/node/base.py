import logging

logger = logging.getLogger(__name__)

class NodeBase:
    """Base class for nodes, which are all the pages that Twitter allows us
    to visit with a simple HTTP client.
    They behave as generators, and yield `PageElement` data as processed
    by the `BeautifulSoup` library."""
    def __init__(self):
        logger.debug("Initializing {}".format(self.__class__.__qualname__))

    def __iter__(self) -> 'PageElement':
        logger.debug("Iterating on {}".format(self.__class__.__qualname__))
