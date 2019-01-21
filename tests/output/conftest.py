import yaml
import pytest

from twhatter.parser import TweetBase, User

@pytest.fixture(scope="session")
def fixtures_factory():
    """Factory for any kind of data that can be stored in YAML format"""
    def _fixtures_factory(yaml_file):
        with open(yaml_file, 'r') as f:
            fixtures = yaml.load(f)
        return fixtures

    return _fixtures_factory


@pytest.fixture(scope="session")
def tweets_factory(fixtures_factory):
    """Factory for tweets from YAML file"""
    def _tweets_factory(yaml_file):
        all_fixtures = fixtures_factory(yaml_file)
        return [t for t in all_fixtures if isinstance(t, TweetBase)]

    return _tweets_factory


@pytest.fixture(scope="session")
def users_factory(fixtures_factory):
    """Factory for tweets from YAML file"""
    def _users_factory(yaml_file):
        all_fixtures = fixtures_factory(yaml_file)
        return [u for u in all_fixtures if isinstance(u, User)]

    return _users_factory

@pytest.fixture
def timeline_mock_factory(tweets_factory, monkeypatch, timeline_attribute):
    def _timeline_mock_factory(tweets_file):
        tweets = tweets_factory(tweets_file)

        class MockClientTimeline:
            def __init__(self, user, limit):
                pass

            def __iter__(self):
                return iter(tweets)
        monkeypatch.setattr(timeline_attribute, MockClientTimeline)

    return _timeline_mock_factory

@pytest.fixture
def profile_mock_factory(users_factory, monkeypatch, profile_attribute):
    def _profile_mock_factory(user_file):
        users = users_factory(user_file)

        # Make a dictionary out of users, indexed by the twitter handle

        class MockClientProfile:
            def __init__(self, user):
                if user in users:
                    self.user = users[user]

        monkeypatch.setattr(profile_attribute,  MockClientProfile)
    return _profile_mock_factory
