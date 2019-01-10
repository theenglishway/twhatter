import pytest
from click.testing import CliRunner
from bs4 import BeautifulSoup

from twhatter.api import ApiUser
from twhatter.parser import TweetList
from typing import NamedTuple

@pytest.fixture
def cli_runner():
    """Runner for Click"""
    return CliRunner()


@pytest.fixture(scope="session")
def user():
    return "the_english_way"


@pytest.fixture(scope="session")
def tweet_limit():
    return 10

# Fixtures for extraction of specific tweets of several kinds, whose author
# and id are known in advance


class TweetInfo(NamedTuple):
    """Class to hold information about a tweet that is already known"""
    id: int
    # Name of the original author
    screen_name: str
    user_id: int
    # Name of the retweeter user
    retweeter: str = None

@pytest.fixture(scope="session")
def tweet_collection():
    return {
        'plain': TweetInfo(
            id=1077838164813848576,
            screen_name="the_english_way",
            user_id=943804775942033408
        ),
        'reaction_tweet': TweetInfo(
            id=1078281840945963008,
            screen_name="the_english_way",
            user_id=943804775942033408
        ),
        'with_link': TweetInfo(
            id=1078281840945963008,
            screen_name="the_english_way",
            user_id=943804775942033408
        ),
        'retweet': TweetInfo(
            id=1055037291108974592,
            screen_name="Senficon",
            user_id=14861745,
            retweeter="the_english_way"
        )
    }


@pytest.fixture(scope="session")
def raw_html_user_initial_page_factory():
    def _raw_html_user_initial_page(user):
        a = ApiUser(user)
        response = a.get_initial()
        return BeautifulSoup(response.text, "lxml")
    return _raw_html_user_initial_page


@pytest.fixture(scope="session")
def raw_html_user_initial_page(raw_html_user_initial_page_factory, user):
    return raw_html_user_initial_page_factory(user)


@pytest.fixture(scope="session")
def raw_tweet_factory(raw_html_user_initial_page_factory):
    def _raw_tweet_factory(tweet_info):
        user_page = tweet_info.retweeter or tweet_info.screen_name
        soup = raw_html_user_initial_page_factory(user_page)
        return soup.find(id="stream-item-tweet-{}".format(tweet_info.id))
    return _raw_tweet_factory
