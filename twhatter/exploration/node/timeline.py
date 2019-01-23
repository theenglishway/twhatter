import logging
import json

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from .base import NodeBase
from twhatter.parser import ParserTweet

logger = logging.getLogger(__name__)


class NodeTimeline(NodeBase):
    """Implementation of the "timeline" node, which is the page accessed by
    https://twitter.com/the_user_name, that can be scrolled until the beginning
    of times."""
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
        logger.info("{} tweets retrieved so far".format(self.nb_tweets))

    @classmethod
    def _get_base_page(cls, user_handle):
        logger.info("Loading base page for {}'s timeline".format(user_handle))
        url = "https://twitter.com/{}".format(user_handle)
        return requests.get(
            url,
            headers={
                'User-Agent': cls.user_agent,
                'Accept-Language': 'en'
            }
        )

    def _scroll(self):
        logger.info("Scrolling in {}'s timeline".format(self.user))
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
        base = self._get_base_page(self.user)
        soup = BeautifulSoup(base.text, "lxml")
        self._update_state(soup)
        yield soup

        while self.nb_tweets < self.limit:
            more = self._scroll()
            html = json.loads(more.content)

            soup = BeautifulSoup(html['items_html'], "lxml")
            if not soup.text:
                logger.info("Latest request provided no explorable content")
                break

            self._update_state(soup)
            yield soup

    def __repr__(self):
        return "<{} (user={}, limit={})>".format(
            self.__class__.__qualname__,
            self.user,
            self.limit
        )
