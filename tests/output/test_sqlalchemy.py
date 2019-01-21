import pytest
from twhatter.output import Database
from twhatter.output.sqlalchemy import Tweet, User

@pytest.fixture
def timeline_attribute():
    return "twhatter.output.sqlalchemy.db.ClientTimeline"

@pytest.fixture
def profile_attribute():
    return "twhatter.output.sqlalchemy.db.ClientProfile"

@pytest.fixture()
def db_url():
    return "sqlite://"

@pytest.fixture(scope="function")
def output(db_url):
    return Database(db_url)

@pytest.mark.parametrize("fixtures_file, expected_len", [
    ('tests/fixtures/tweets/text_only_10.yaml', 10),
    ('tests/fixtures/tweets/retweet_10.yaml', 10),
    ('tests/fixtures/tweets/link_10.yaml', 10),
    ('tests/fixtures/tweets/reaction_9.yaml', 9),
])
def test_output_tweets(capsys, timeline_mock_factory, profile_mock_factory, output, fixtures_file, expected_len):
    timeline_mock_factory(fixtures_file)
    profile_mock_factory(fixtures_file)
    output.output_tweets(None, None)

    session = output.session_maker()
    assert session.query(Tweet).count() == expected_len
