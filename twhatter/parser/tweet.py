from datetime import datetime

from bs4 import BeautifulSoup
from dataclasses import dataclass, fields, field


@dataclass
class Tweet:
    #timestamp: datetime
    user: str
    #fullname: fullname
    id: int
    #url: url
    timestamp: datetime
    #text: str
    #replies: int
    retweets: int
    #quoted_tweet: int
    likes: int
    #html: str
    #soup: Any
    soup: BeautifulSoup = field(repr=False)

    @staticmethod
    def extract_id(soup):
        return int(soup['data-item-id'])

    @staticmethod
    def extract_timestamp(soup):
        return datetime.utcfromtimestamp(
            int(soup.find('span', '_timestamp')['data-time'])
        )

    @staticmethod
    def extract_user(soup):
        return soup.find('span', 'username').text or ""

    @staticmethod
    def extract_fullname(soup):
        return soup.find('strong', 'fullname').text or ""

    @staticmethod
    def extract_retweets(soup):
        return int(soup.find(
                    'span', 'ProfileTweet-action--retweet u-hiddenVisually')
                       .find(
                    'span', 'ProfileTweet-actionCount'
                    )['data-tweet-stat-count']
                   )

    @staticmethod
    def extract_quoted_tweet(soup):
        return int(soup.find(
            'span', 'QuoteTweet-innerContainer').find(
                'span', 'ProfileTweet-actionCount')['data-tweet-stat-count']),

    @staticmethod
    def extract_soup(soup):
        return soup

    @classmethod
    def extract(cls, soup):
        def _extract_value(field):
            fn = getattr(cls, "extract_{}".format(field.name), None)
            if not fn:
                raise NotImplementedError(
                    "Extract function for field '{}' is not "
                    "implemented".format(field.name)
                )

            return fn(soup)

        kwargs = {f.name: _extract_value(f) for f in fields(cls)}
        return cls(**kwargs)


class TweetList:
    def __init__(self, soup):
        self.raw_tweets = soup.find_all('li', 'stream-item')

    def __iter__(self):
        for tweet in self.raw_tweets:
            yield Tweet.extract(tweet)
