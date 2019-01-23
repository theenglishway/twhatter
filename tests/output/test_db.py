import pytest
from twhatter.output import Database
from twhatter.output.sqlalchemy import Tweet


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

@pytest.mark.parametrize("fixtures_file", [
    'tests/fixtures/tweets/text_only_10.yaml',
    'tests/fixtures/tweets/retweet_10.yaml',
    'tests/fixtures/tweets/link_10.yaml',
    'tests/fixtures/tweets/reaction_9.yaml',
], ids=[
    "TextOnly",
    "Retweet",
    "Link",
    "Reaction"
])
def test_output_tweets_presence(capsys, tweets_factory, output, fixtures_file, session):
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
