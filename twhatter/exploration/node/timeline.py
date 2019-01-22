import logging
import json

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from .base import NodeBase
from twhatter.parser import ParserTweet

logger = logging.getLogger(__name__)


class NodeTimeline(NodeBase):
    user_agent = generate_user_agent(os='linux')

    def __init__(self, user, limit=100):
        super().__init__()
        self.user = user
        self.earliest_tweet_id = None
        self.nb_tweets = 0
        self.limit = limit

    def _update_state(self, soup):
        tweets = ParserTweet(soup)
        self.nb_tweets += len(tweets)
        *_, self.earliest_tweet_id = (t.id for t in tweets)

    @classmethod
    def get_user_timeline(cls, user_handle):
        logger.info("Loading initial timeline for {}".format(user_handle))
        url = "https://twitter.com/{}".format(user_handle)
        return requests.get(
            url,
            headers={
                'User-Agent': cls.user_agent,
                'Accept-Language': 'en'
            }
        )

    def get_more_tweets(self):
        logger.info("Loading more tweets from {}".format(self.user))
        return requests.get(
            "https://twitter.com/i/profiles/show/{}/timeline/tweets".format(self.user),
            params= dict(
                include_available_features=1,
                include_entities=1,
                max_position=self.earliest_tweet_id,
                reset_error_state=False
            ),
            headers={'User-Agent': self.user_agent}
        )

    def __iter__(self):
        super().__iter__()
        tweets = self.get_user_timeline(self.user)
        soup = BeautifulSoup(tweets.text, "lxml")
        self._update_state(soup)
        yield soup

        while True and self.nb_tweets < self.limit:
            more_tweets = self.get_more_tweets()
            html = json.loads(more_tweets.content)

            soup = BeautifulSoup(html['items_html'], "lxml")
            if not soup.text:
                break

            self._update_state(soup)
            yield soup

    def __repr__(self):
        return "<{} (user={}, limit={})>".format(
            self.__class__.__qualname__,
            self.user,
            self.limit
        )
