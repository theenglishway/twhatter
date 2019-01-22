import logging

logger = logging.getLogger(__name__)

class NodeBase:
    """Base class for nodes, which are all the pages that Twitter allows us
    to visit. They can be iterated on, and will yield data within the limits
    defined at initialization"""
    def __init__(self):
        logger.debug("Initializing {}".format(self.__class__.__qualname__))

    # TODO: there should be one function per kind of object (iter_tweets,
    #  iter_users, ...)
    def __iter__(self):
        logger.debug("Iterating on {}".format(self.__class__.__qualname__))
