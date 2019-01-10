import requests
from random import choice
from bs4 import BeautifulSoup

from twhatter.parser import TweetList, user_factory
import json


class Client():
    HEADERS_LIST = [
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
        'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
    ]

    @classmethod
    def get_user_timeline(cls, user_handle):
        url = "https://twitter.com/{}".format(user_handle)
        return requests.get(
            url,
            headers={
                'User-Agent': choice(cls.HEADERS_LIST),
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
            headers={'User-Agent': choice(self.HEADERS_LIST)}
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
