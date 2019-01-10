from datetime import datetime

from bs4 import BeautifulSoup
from dataclasses import dataclass, fields, InitVar, field


@dataclass
class Tweet:
    #: Tweet ID
    id: int
    #: Handle of the tweet's original author
    screen_name: str
    #: ID of the tweet's original author
    user_id: int
    timestamp: datetime
    replies: int
    retweets: int
    likes: int
    text: str = field(repr=False)
    #: Handle of the tweet's retweeter
    retweeter: str = None
    soup: InitVar[BeautifulSoup] = None

    def __post_init__(self, soup):
        self.soup = soup

    @staticmethod
    def _extract_data(soup, distinct_span, data_kw):
        return (
            soup.find('span', distinct_span)
                .find('span', attrs={data_kw: True})
            [data_kw]
        )

    @staticmethod
    def _extract_from_div_tweet(soup, data_kw):
        kw = "data-{}".format(data_kw)
        return(
            soup.find('div', class_='tweet', attrs={kw: True})[kw]
        )

    @staticmethod
    def extract_id(soup):
        return int(soup['data-item-id'])

    @classmethod
    def extract_screen_name(cls, soup):
        return cls._extract_from_div_tweet(soup, 'screen-name')

    @classmethod
    def extract_user_id(cls, soup):
        return int(cls._extract_from_div_tweet(soup, 'user-id'))

    @classmethod
    def extract_retweeter(cls, soup):
        try:
            return cls._extract_from_div_tweet(soup, 'retweeter')
        except TypeError:
            return None

    @staticmethod
    def extract_timestamp(soup):
        return datetime.utcfromtimestamp(
            int(soup.find('span', attrs={'data-time': True})['data-time'])
        )

    @staticmethod
    def extract_fullname(soup):
        return soup.find('strong', 'fullname').text

    @classmethod
    def extract_retweets(cls, soup):
        return cls._extract_data(
            soup,
            'ProfileTweet-action--retweet',
            'data-tweet-stat-count'
        )

    @classmethod
    def extract_replies(cls, soup):
        return cls._extract_data(
            soup,
            'ProfileTweet-action--reply',
            'data-tweet-stat-count'
        )

    @classmethod
    def extract_likes(cls, soup):
        return cls._extract_data(
            soup,
            'ProfileTweet-action--favorite',
            'data-tweet-stat-count'
        )

    @staticmethod
    def extract_text(soup):
        return soup.find('p', 'tweet-text').text

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
        return cls(soup=soup, **kwargs)


class TweetList:
    def __init__(self, soup):
        self.raw_tweets = soup.find_all('li', 'stream-item')

    def __iter__(self):
        for tweet in self.raw_tweets:
            # Don't know what this u-dir stuff is about but if it's in there,
            # it's not a tweet !
            if not tweet.find_all('p', class_="u-dir"):
                yield Tweet.extract(tweet)

    def __len__(self):
        return len(self.raw_tweets)
