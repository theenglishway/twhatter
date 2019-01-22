from typing import List


class OutputBase:
    """Base class for scraper's data output"""
    def start(self):
        pass

    def output_tweets(self, tweets: List['TweetBase']) -> None:
        raise NotImplementedError()

    def output_users(self, users: List['User']) -> None:
        raise NotImplementedError()

    def output_medias(self, medias: List['MediaBase']) -> None:
        raise NotImplementedError()

    def stop(self):
        pass
