import logging
from datetime import datetime

from bs4 import BeautifulSoup
from dataclasses import dataclass, fields, InitVar, field
from typing import List

from .base import ParserBase
from .mixins import ExtractableMixin
from .media import MediaBase, media_factory


logger = logging.getLogger(__name__)


@dataclass
class TweetBase(ExtractableMixin):
    #: Tweet ID
    id: int
    #: Tweeter handle of the tweet's author (the handle used for URLs)
    username: str
    #: Name of the tweet's author (the name as it appears on-screen)
    fullname: str
    #: ID of the tweet's original author
    user_id: int
    #: Number of comments
    comments_nb: int
    #: Number of retweets
    retweets_nb: int
    #: Number of likes
    likes_nb: int
    #: Timestamp of the original tweet
    timestamp: datetime
    #: Permalink to the original tweet
    permalink: str
    #: Text of the tweet
    text: str = field(repr=False)
    #: List of hashtags in the tweet
    hashtag_list: List[str]
    #: List of mentions in the tweet
    mention_list: List[int]

    #: Handle of the tweet's retweeter
    retweeter: str = None
    #: Id of the retweet
    retweet_id: int = None

    #: Id of the tweet that the tweet is in reaction to
    reacted_id: int = None
    #: Id of the user that the tweet is in reaction to
    reacted_user_id: int = None

    #: Link contained within the tweet
    link_to: str = None

    #: Media that the tweet contains
    media: MediaBase = None

    #: The soup extracted from the raw HTML
    soup: InitVar[BeautifulSoup] = None

    def __repr__(self):
        return ("<{0} "
                "(id={1.id}, "
                "date={1.timestamp}, "
                "likes={1.likes_nb}, "
                "retweets={1.retweets_nb}, "
                "comments={1.comments_nb})>".format(self.__class__.__qualname__, self))

    @staticmethod
    def condition(kwargs: dict) -> bool:
        raise NotImplementedError()

    @classmethod
    def _extract_from_div_tweet(cls, soup, data_kw):
        return cls._extract_from_div(soup, 'tweet', data_kw)

    @staticmethod
    def extract_id(soup):
        return int(soup['data-item-id'])

    @classmethod
    def extract_username(cls, soup):
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

    @classmethod
    def extract_retweet_id(cls, soup):
        try:
            return int(cls._extract_from_div_tweet(soup, 'retweet-id'))
        except TypeError:
            return None

    @classmethod
    def extract_reacted_id(cls, soup):
        try:
            return int(cls._extract_from_div(soup, 'QuoteTweet-innerContainer', 'item-id'))
        except TypeError:
            return None

    @classmethod
    def extract_reacted_user_id(cls, soup):
        try:
            return int(cls._extract_from_div(soup, 'QuoteTweet-innerContainer', 'user-id'))
        except TypeError:
            return None

    @classmethod
    def extract_link_to(cls, soup):
        try:
            return cls._extract_from_div(soup, 'card-type-summary', 'card-url')
        except TypeError:
            return None

    @staticmethod
    def extract_timestamp(soup):
        return datetime.utcfromtimestamp(
            int(soup.find('span', attrs={'data-time': True})['data-time'])
        )

    @classmethod
    def extract_permalink(cls, soup):
        return cls._extract_from_div_tweet(soup, 'permalink-path')

    @staticmethod
    def extract_fullname(soup):
        return soup.find('strong', 'fullname').text

    @classmethod
    def extract_retweets_nb(cls, soup):
        return int(cls._extract_from_span(
            soup,
            'ProfileTweet-action--retweet',
            'data-tweet-stat-count'
        ))

    @classmethod
    def extract_comments_nb(cls, soup):
        return int(cls._extract_from_span(
            soup,
            'ProfileTweet-action--reply',
            'data-tweet-stat-count'
        ))

    @classmethod
    def extract_likes_nb(cls, soup):
        return int(cls._extract_from_span(
            soup,
            'ProfileTweet-action--favorite',
            'data-tweet-stat-count'
        ))

    @staticmethod
    def extract_hashtag_list(soup):
        return [
            link.b.text
            for link in soup.find_all('a', class_="twitter-hashtag")
        ]

    @staticmethod
    def extract_mention_list(soup):
        data_kw="data-mentioned-user-id"
        return [
            int(value[data_kw])
            for value in soup.find_all(
                'a',
                class_="twitter-atreply",
                attrs={data_kw: True}
            )
        ]

    @staticmethod
    def extract_text(soup):
        return soup.find('p', 'tweet-text').text

    @staticmethod
    def extract_media(soup):
        return media_factory(soup.find('div', 'AdaptiveMedia'))


class TweetTextOnly(TweetBase):
    """An original tweet with only plain text"""


class TweetLink(TweetBase):
    """An original tweet with a link"""
    @staticmethod
    def condition(kwargs):
        return kwargs['link_to']

    def __repr__(self):
        return ("<{0} "
                "(id={1.id}, "
                "date={1.timestamp}, "
                "likes={1.likes_nb}, "
                "retweets={1.retweets_nb}, "
                "comments={1.comments_nb}, "
                "link_to={1.link_to})>".format(self.__class__.__qualname__, self))

class TweetRetweet(TweetBase):
    """A plain retweet"""
    @staticmethod
    def condition(kwargs):
        return kwargs['retweet_id']

    def __repr__(self):
        return ("<{0} "
                "(id={1.id}, "
                "date={1.timestamp}, "
                "likes={1.likes_nb}, "
                "retweets={1.retweets_nb}, "
                "comments={1.comments_nb}, "
                "retweeter={1.retweeter}, "
                "retweet_id={1.retweet_id})>".format(self.__class__.__qualname__, self))

class TweetReaction(TweetBase):
    """A reaction to another tweet"""
    @staticmethod
    def condition(kwargs):
        return kwargs['reacted_id']

    def __repr__(self):
        return ("<{0} "
                "(id={1.id}, "
                "date={1.timestamp}, "
                "likes={1.likes_nb}, "
                "retweets={1.retweets_nb}, "
                "comments={1.comments_nb}, "
                "reacted_id={1.reacted_id}, "
                "reacted_user_id={1.reacted_user_id})>".format(self.__class__.__qualname__, self))

def tweet_factory(soup: BeautifulSoup) -> TweetBase:
    """
    :param soup: the soup extracted from the raw html for that tweet
    :return: a well-formatted Tweet
    """
    kwargs = {
        f.name: TweetBase._extract_value(soup, f) for f in fields(TweetBase)
    }

    for kls in TweetBase.__subclasses__():
        try:
            if kls.condition(kwargs):
                return kls(soup=soup, **kwargs)
        except NotImplementedError:
            continue
    else:
        return TweetTextOnly(soup=soup, **kwargs)


class TweetList:
    def __init__(self, soup):
        self.raw_tweets = soup.find_all('li', 'stream-item')

    def __iter__(self):
        for tweet in self.raw_tweets:
            # Don't know what this u-dir stuff is about but if it's in there,
            # it's not a tweet !
            if not tweet.find_all('p', class_="u-dir"):
                t = tweet_factory(tweet)
                logger.debug("Parsed tweet {}".format(t))
                yield t

    def __len__(self):
        return len(self.raw_tweets)


class ParserTweet(ParserBase):
    def __init__(self, soup):
        super().__init__(soup)
        self.raw_tweets = soup.find_all('li', 'stream-item')

    def __iter__(self):
        for tweet in self.raw_tweets:
            # Don't know what this u-dir stuff is about but if it's in there,
            # it's not a tweet !
            if not tweet.find_all('p', class_="u-dir"):
                t = tweet_factory(tweet)
                logger.debug("Parsed tweet {}".format(t))
                yield t

    def __len__(self):
        return len(self.raw_tweets)
