import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from twhatter.parser import TweetList, user_factory
import json


class Client():
    user_agent = generate_user_agent(os='linux')

    @classmethod
    def get_user_timeline(cls, user_handle):
        url = "https://twitter.com/{}".format(user_handle)
        return requests.get(
            url,
            headers={
                'User-Agent': cls.user_agent,
                'Accept-Language': 'en'
            }
        )


class ClientTimeline(Client):
    """Access and explore some user's timeline"""
    def __init__(self, user, limit=100):
        self.user = user
        self.earliest_tweet = None
        self.nb_tweets = 0
        self.limit = limit

    def get_more_tweets(self):
        return requests.get(
            "https://twitter.com/i/profiles/show/{}/timeline/tweets".format(self.user),
            params= dict(
                include_available_features=1,
                include_entities=1,
                max_position=self.earliest_tweet,
                reset_error_state=False
            ),
            headers={'User-Agent': self.user_agent}
        )

    def __iter__(self):
        tweets = self.get_user_timeline(self.user)
        soup = BeautifulSoup(tweets.text, "lxml")
        t_list = TweetList(soup)

        for t in t_list:
            yield t
            self.earliest_tweet = t.id
            self.nb_tweets += 1

        while True and self.nb_tweets < self.limit:
            more_tweets = self.get_more_tweets()
            html = json.loads(more_tweets.content)
            soup = BeautifulSoup(html['items_html'], "lxml")
            t_list = TweetList(soup)

            if len(t_list) == 0:
                break

            for t in t_list:
                yield t
                self.earliest_tweet = t.id
                self.nb_tweets += 1


class ClientProfile(Client):
    """Get profile information about an user"""
    def __init__(self, user_handle):
        self.user_handle = user_handle
        user_page = self.get_user_timeline(user_handle)
        soup = BeautifulSoup(user_page.text, "lxml")

        self.user = user_factory(soup)
