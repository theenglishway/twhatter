import logging
from datetime import datetime

from bs4 import BeautifulSoup
from dataclasses import dataclass, fields, InitVar

from .mixins import ExtractableMixin
from .base import ParserBase


logger = logging.getLogger(__name__)


@dataclass
class User(ExtractableMixin):
    #: User ID
    id: int
    #: Tweeter handle (the one used for URLs)
    username: str
    # Name as it appears on screen
    fullname: str
    # Date at which the user joined
    join_date: datetime
    # Total number of tweets
    tweets_nb: int
    # Total number of accounts followed
    following_nb: int
    # Total number of followers
    followers_nb: int
    # Total number of likes sent by this user
    likes_nb: int

    #: The soup extracted from the raw HTML
    soup: InitVar[BeautifulSoup] = None

    @staticmethod
    def _extract_from_li(soup, distinct_span, kw):
        data_kw = "data-{}".format(kw)
        return (
            soup.find('li', distinct_span)
                .find('span', attrs={data_kw: True})
            [data_kw]
        )

    @classmethod
    def extract_id(cls, soup):
        id_str = cls._extract_from_div(soup, 'ProfileNav', 'user-id')
        if not id_str:
            raise ValueError("No id could be found")

        return int(id_str)

    @classmethod
    def extract_fullname(cls, soup):
        return soup.find('a', 'ProfileHeaderCard-nameLink').text

    @classmethod
    def extract_username(cls, soup):
        return soup.find('b', 'u-linkComplex-target').text

    @classmethod
    def extract_join_date(cls, soup):
        kw = 'title'
        datetime_str = soup.find(
            'span',
            class_='ProfileHeaderCard-joinDateText',
            attrs={kw: True}
        )[kw]

        # The date is in a weird format (e.g. "7:27 AM - 8 May 2011") and we
        # don't really care for the exact hour so we only keep the date
        day_str = datetime_str.split(' - ')[1]
        return datetime.strptime(day_str, '%d %b %Y')

    @classmethod
    def extract_tweets_nb(cls, soup):
        return int(cls._extract_from_li(soup, 'ProfileNav-item--tweets', 'count'))

    @classmethod
    def extract_following_nb(cls, soup):
        return int(cls._extract_from_li(soup, 'ProfileNav-item--following', 'count'))

    @classmethod
    def extract_followers_nb(cls, soup):
        return int(cls._extract_from_li(soup, 'ProfileNav-item--followers', 'count'))

    @classmethod
    def extract_likes_nb(cls, soup):
        return int(cls._extract_from_li(soup, 'ProfileNav-item--favorites', 'count'))


class ParserUser(ParserBase):
    def __init__(self, soup):
        self.soup = soup

    def __iter__(self):
        try:
            kwargs = {
                f.name: User._extract_value(self.soup, f) for f in fields(User)
            }
        except ValueError:
            logger.debug("Soup contained no data for {}".format(self))
            return

        u = User(**kwargs)
        logger.debug("Parsed user {}".format(u))
        yield u

    def __len__(self):
        return 1
