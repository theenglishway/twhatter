import pytest
from twhatter.parser import TweetList, Tweet


class TestTweetList:
    def test_len(self, raw_html_user_initial_page):
        t_list = TweetList(raw_html_user_initial_page)
        assert len(t_list) == 20

    def test_iter(self, raw_html_user_initial_page):
        t_list = TweetList(raw_html_user_initial_page)
        for t in t_list:
            assert isinstance(t, Tweet)


class TestTweet:
    @pytest.mark.parametrize("tweet_type", [
        "plain",
        "reaction_tweet",
        "with_link",
    ])
    def test_plain_tweet(self, raw_tweet_factory, tweet_collection, tweet_type):
        tweet_info = tweet_collection[tweet_type]
        raw = raw_tweet_factory(tweet_info)
        t = Tweet.extract(raw)
        assert t

        for field, value in tweet_info._asdict().items():
            assert getattr(t, field) == value
