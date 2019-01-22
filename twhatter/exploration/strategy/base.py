import logging

logger = logging.getLogger(__name__)

class StrategyBase:
    """Base class for strategies, which define a way to explore Tweeter pages"""
    def __init__(self, starting_node: 'NodeBase') -> None:
        logger.debug(
            "Initializing {} with starting_node={}".format(
                self.__class__.__qualname__,
                starting_node
            )
        )
        self.starting_node = starting_node

    def __call__(self, output) -> None:
        logger.debug("Applying {}".format(self.__class__.__qualname__))
