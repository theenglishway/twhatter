import pytest
from datetime import datetime

from click.testing import CliRunner
from bs4 import BeautifulSoup

from twhatter.exploration import NodeTimeline
from twhatter.parser import tweet_factory
from typing import NamedTuple, List

from twhatter.parser.media import MediaBase

@pytest.fixture
def cli_runner():
    """Runner for Click"""
    return CliRunner()


@pytest.fixture(scope="session")
def user():
    return "the_english_way"


@pytest.fixture(scope="session")
def user_prolific():
    return "realDonaldTrump"


@pytest.fixture(scope="session")
def tweet_limit():
    return 10

# Fixtures for extraction of specific tweets of several kinds, whose author
# and id are known in advance

class MediaInfo(NamedTuple):
    """Class to hold information about a media that is already known"""
    image_links: List[str] = []

    def __eq__(self, other):
        """Override of __eq__ to check against `MediaBase` instance"""
        return (isinstance(other, MediaBase)
                and other.image_links == self.image_links)


class TweetInfo(NamedTuple):
    """Class to hold information about a tweet that is already known"""
    id: int
    username: str
    fullname: str
    user_id: int
    permalink: str
    timestamp: datetime = None
    text: str = None
    comments_nb: int = None
    retweets_nb: int = None
    likes_nb: int = None
    hashtag_list: List[str] = None
    mention_list: List[int] = None
    retweeter: str = None
    retweet_id: int = None
    reacted_id: int = None
    reacted_user_id: int = None
    link_to: str = None
    media: MediaInfo = None


@pytest.fixture(scope="session")
def tweet_collection():
    return {
        'plain': TweetInfo(
            id=1077838164813848576,
            username="the_english_way",
            fullname="theenglishway",
            user_id=943804775942033408,
            timestamp=datetime.utcfromtimestamp(1545811618),
            permalink="/the_english_way/status/1077838164813848576",
            text="""Ca y est j'ai un pipeline Concourse avec un job qui builde une image @Docker qui affiche un "Hello World" dans un autre job \o/
........... je suis pas sûr de savoir ce que ça veut dire, mais en tout cas c'était mon objectif de la matinée """
        ),
        'reaction_tweet': TweetInfo(
            id=1078281840945963008,
            username="the_english_way",
            fullname="theenglishway",
            user_id=943804775942033408,
            timestamp=datetime.utcfromtimestamp(1545917399),
            permalink="/the_english_way/status/1078281840945963008",
            reacted_id=1078277316193726464,
            reacted_user_id=19976004
        ),
        'with_link': TweetInfo(
            id=1077505613079429120,
            username="the_english_way",
            fullname="theenglishway",
            user_id=943804775942033408,
            timestamp=datetime.utcfromtimestamp(1545732331),
            permalink="/the_english_way/status/1077505613079429120",
            link_to="https://t.co/el5VJucLRz"
        ),
        'retweet': TweetInfo(
            id=1055037291108974592,
            username="Senficon",
            fullname="Julia Reda",
            user_id=14861745,
            retweeter="the_english_way",
            retweet_id=1055098556300828672,
            timestamp=datetime.utcfromtimestamp(1540375466),
            permalink="/Senficon/status/1055037291108974592",
        ),
        'hashtags': TweetInfo(
            id=1039969574555471873,
            username="BurgerQuizOff",
            fullname="Burger Quiz",
            user_id=949604705772228608,
            retweeter="the_english_way",
            permalink="/BurgerQuizOff/status/1039969574555471873",
            hashtag_list=["Nuggets", "BurgerQuiz", "PrivacyMonCul"]
        ),
        'mentions': TweetInfo(
            id=1077838164813848576,
            username="the_english_way",
            fullname="theenglishway",
            user_id=943804775942033408,
            timestamp=datetime.utcfromtimestamp(1545811618),
            permalink="/the_english_way/status/1077838164813848576",
            mention_list=[1138959692]
        ),
        'stats': TweetInfo(
            id=1039969574555471873,
            username="BurgerQuizOff",
            fullname="Burger Quiz",
            user_id=949604705772228608,
            permalink="/BurgerQuizOff/status/1039969574555471873",
            retweeter="the_english_way",
            comments_nb=12,
            retweets_nb=176,
            likes_nb=555
        ),
        'media':TweetInfo(
            id=1086327536726900736,
            username="the_english_way",
            fullname="theenglishway",
            user_id=943804775942033408,
            permalink="/the_english_way/status/1086327536726900736",
            media=MediaInfo(
                image_links=["https://pbs.twimg.com/media/DxNof6AXQAAu2oU.jpg"]
            )
        ),
    }


@pytest.fixture(scope="session")
def raw_html_user_initial_page_factory():
    def _raw_html_user_initial_page(user):
        n = NodeTimeline(user)
        response = n.get_user_timeline(user)
        return BeautifulSoup(response.text, "lxml")
    return _raw_html_user_initial_page


@pytest.fixture(scope="session")
def raw_html_user_initial_page(raw_html_user_initial_page_factory, user):
    return raw_html_user_initial_page_factory(user)


@pytest.fixture(scope="session")
def raw_tweet_factory(raw_html_user_initial_page_factory):
    def _raw_tweet_factory(tweet_info):
        user_page = tweet_info.retweeter or tweet_info.username
        soup = raw_html_user_initial_page_factory(user_page)
        return soup.find(id="stream-item-tweet-{}".format(tweet_info.id))

    return _raw_tweet_factory


@pytest.fixture(scope="session")
def tweet_test_data_factory(raw_tweet_factory, tweet_collection):
    def _tweet_test_data_factory(tweet_type):
        tweet_info = tweet_collection[tweet_type]
        raw_tweet = raw_tweet_factory(tweet_info)
        return tweet_factory(raw_tweet), tweet_info

    return _tweet_test_data_factory


class UserInfo(NamedTuple):
    """Class to hold information about an user that is already known"""
    id: int
    fullname: str
    username: str
    join_date: datetime
    tweets_nb: int = None
    following_nb: int = None
    followers_nb: int = None
    likes_nb: int = None


@pytest.fixture(scope="session")
def user_collection():
    return {
        'Marlene_beadles': UserInfo(
            id=295177446,
            username="Marlene_beadles",
            fullname="Marlene Hansen",
            join_date=datetime(2011, 5, 8, 0, 0),
            tweets_nb=25,
            following_nb=342,
            followers_nb=81,
            likes_nb=4
        ),
        'the_english_way': UserInfo(
            id=943804775942033408,
            fullname="theenglishway",
            username="the_english_way",
            join_date=datetime(2017, 12, 21, 0, 0),
        ),
    }
