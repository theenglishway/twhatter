import pytest
from click.testing import CliRunner
from twhatter.api import ApiUser
from bs4 import BeautifulSoup


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


@pytest.fixture(scope="session")
def raw_html_user_initial_page(user):
    a = ApiUser(user)
    response = a.get_initial()
    return BeautifulSoup(response.text, "lxml")
