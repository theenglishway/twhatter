from .base import StrategyBase
from twhatter.parser import TweetBase, User


class StrategyDumb(StrategyBase):
    """This strategy only explores the initial node"""
    def __call__(self, output):
        super().__call__(output)
        output.start()

        tweets = [t for t in self.starting_node if isinstance(t, TweetBase)]
        output.output_tweets(tweets)
        users = [u for u in self.starting_node if isinstance(u, User)]
        output.output_users(users)

        output.stop()
