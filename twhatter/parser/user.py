import logging
from datetime import datetime

from bs4 import BeautifulSoup
from dataclasses import dataclass, fields, InitVar

from .mixins import ExtractableMixin


logger = logging.getLogger(__name__)


@dataclass
class User(ExtractableMixin):
    id: int
    screen_name: str
    join_date: datetime
    tweets_nb: int
    following_nb: int
    followers_nb: int
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
        return int(cls._extract_from_div(soup, 'ProfileNav', 'user-id'))

    @classmethod
    def extract_screen_name(cls, soup):
        return soup.find('a', 'ProfileHeaderCard-nameLink').text

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


def user_factory(soup: BeautifulSoup) -> User:
    kwargs = {
        f.name: User._extract_value(soup, f) for f in fields(User)
    }
    u = User(**kwargs)
    logger.debug("Parsed user {}".format(u))
    return u
