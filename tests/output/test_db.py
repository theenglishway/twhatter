import pytest
from dataclasses import fields

from twhatter.output import Database
from twhatter.output.sqlalchemy import Tweet
from twhatter.parser.tweet import *


@pytest.fixture
def db_url():
    return "sqlite://"


@pytest.fixture(scope="function")
def output(db_url):
    return Database(db_url)


@pytest.fixture(scope="function")
def session(output):
    session = output.session_maker()
    yield session
    session.close()


@pytest.fixture(scope="function")
def tweets_output_factory(tweets_factory, output):
    """Tweets that have been output"""
    def _tweets_output_factory(fixtures_file):
        tweets = tweets_factory(fixtures_file)
        output.start()
        output.output_tweets(tweets)
        output.stop()
        return tweets
    return _tweets_output_factory


testdata = [
    pytest.param('tests/fixtures/tweets/text_only_10.yaml', TweetTextOnly, id="text-only"),
    pytest.param('tests/fixtures/tweets/retweet_10.yaml', TweetRetweet, id="retweets"),
    pytest.param('tests/fixtures/tweets/link_10.yaml', TweetLink, id="link"),
    pytest.param('tests/fixtures/tweets/reaction_9.yaml', TweetReaction, id="reaction"),
]


@pytest.mark.parametrize("fixtures_file, raw_class", testdata)
def test_output_tweets_presence(tweets_factory, output, fixtures_file, session, raw_class):
    tweets = tweets_factory(fixtures_file)
    output.start()
    output.output_tweets(tweets)
    output.stop()

    for t in tweets:
        assert session.query(Tweet).filter(Tweet.id == t.id).one()


@pytest.mark.parametrize("fixtures_file, raw_class", testdata)
def test_output_tweets_twice(tweets_factory, output, fixtures_file, session, raw_class):
    tweets = tweets_factory(fixtures_file)
    output.start()
    output.output_tweets(tweets)
    output.stop()

    output.start()
    output.output_tweets(tweets)
    output.stop()

    for t in tweets:
        assert session.query(Tweet).filter(Tweet.id == t.id).one()


@pytest.mark.parametrize("field_name, fixtures_file, raw_tweet_cls", [
    pytest.param(
        field.name,
        *td.values,
        id="{}-{}".format(td.id, field.name)
    )
    for td in testdata
    for field in fields(TweetTextOnly)
    if field.name != 'media'
])
def test_output_tweets_attributes(tweets_output_factory, fixtures_file, session, raw_tweet_cls, field_name):
    tweets = tweets_output_factory(fixtures_file)

    for t in tweets:
        db_tweet = session.query(Tweet).filter(Tweet.id == t.id).one()
        assert getattr(db_tweet, field_name) == getattr(t, field_name)
