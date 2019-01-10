import pytest
from twhatter.parser import *


class TestTweetList:
    def test_len(self, raw_html_user_initial_page):
        t_list = TweetList(raw_html_user_initial_page)
        assert len(t_list) == 20

    def test_iter(self, raw_html_user_initial_page):
        t_list = TweetList(raw_html_user_initial_page)
        for t in t_list:
            assert isinstance(t, TweetBase)


class TestTweet:
    all_types = [
        "plain",
        "reaction_tweet",
        "with_link",
        "retweet",
        "hashtags",
        "mentions",
        "stats",
    ]

    @pytest.mark.parametrize("tweet_type", all_types)
    def test_tweet(self, raw_tweet_factory, tweet_collection, tweet_type):
        tweet_info = tweet_collection[tweet_type]
        raw = raw_tweet_factory(tweet_info)
        t = TweetBase.extract(raw)
        assert t

        for field, value in tweet_info._asdict().items():
            # It would be rather complicated to keep some test fixtures values
            # accurate (e.g. number of likes, retweets, ...) so for most
            # of them, the expected values are not set on purpose and therefore
            # not tested
            if value is not None:
                assert getattr(t, field) == value

    @pytest.mark.parametrize("tweet_type,expected_class", [
        ('plain', TweetTextOnly),
        ('reaction_tweet', TweetReaction),
        ('with_link', TweetLink),
        ('retweet', TweetRetweet)
    ])
    def test_tweet_type(self, raw_tweet_factory, tweet_collection, tweet_type, expected_class):
        tweet_info = tweet_collection[tweet_type]
        raw = raw_tweet_factory(tweet_info)
        t = TweetBase.extract(raw)
        assert isinstance(t, expected_class)
