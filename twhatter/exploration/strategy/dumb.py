import logging

from .base import StrategyBase
from twhatter.parser import TweetBase, User


logger = logging.getLogger(__name__)


class StrategyDumb(StrategyBase):
    """This strategy only explores the initial node and scrolls through it
    until exhaustion"""
    def __call__(self, output):
        super().__call__(output)
        output.start()

        objs = []
        for s in self.starting_node:
            logger.debug("Got new soup from {}".format(self.starting_node))
            for parser in self.parser_classes:
                logger.debug("Parsing new soup with {}".format(parser))
                for o in parser(s):
                    objs.append(o)

        tweets = [t for t in objs if isinstance(t, TweetBase)]
        output.output_tweets(tweets)
        users = [u for u in objs if isinstance(u, User)]
        output.output_users(users)

        output.stop()
