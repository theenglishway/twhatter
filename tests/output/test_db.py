import pytest
from twhatter.output import Database
from twhatter.output.sqlalchemy import Tweet


@pytest.fixture
def db_url():
    return "sqlite://"


@pytest.fixture(scope="function")
def output(db_url):
    return Database(db_url)


@pytest.mark.parametrize("fixtures_file", [
    'tests/fixtures/tweets/text_only_10.yaml',
    'tests/fixtures/tweets/retweet_10.yaml',
    'tests/fixtures/tweets/link_10.yaml',
    'tests/fixtures/tweets/reaction_9.yaml',
])
def test_output_tweets(capsys, tweets_factory, output, fixtures_file):
    tweets = tweets_factory(fixtures_file)
    output.start()
    output.output_tweets(tweets)
    output.stop()

    session = output.session_maker()
    for t in tweets:
        assert session.query(Tweet).filter(Tweet.id == t.id).one()


@pytest.mark.parametrize("fixtures_file", [
    'tests/fixtures/tweets/text_only_10.yaml',
    'tests/fixtures/tweets/retweet_10.yaml',
    'tests/fixtures/tweets/link_10.yaml',
    'tests/fixtures/tweets/reaction_9.yaml',
])
def test_output_tweets_twice(capsys, tweets_factory, output, fixtures_file):
    tweets = tweets_factory(fixtures_file)
    output.start()
    output.output_tweets(tweets)
    output.stop()

    output.start()
    output.output_tweets(tweets)
    output.stop()

    session = output.session_maker()
    for t in tweets:
        assert session.query(Tweet).filter(Tweet.id == t.id).one()
