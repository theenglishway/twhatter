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
        "media",
    ]

    @pytest.mark.parametrize("tweet_type", all_types)
    def test_tweet(self, tweet_test_data_factory, tweet_type):
        t, tweet_info = tweet_test_data_factory(tweet_type)

        for field, value in tweet_info._asdict().items():
            # It would be rather complicated to keep some test fixtures values
            # accurate (e.g. number of likes, retweets, ...) so for most
            # of them, the expected values are not set on purpose and therefore
            # not tested
            if value is not None:
                assert value == getattr(t, field)

    @pytest.mark.parametrize("tweet_type,expected_class", [
        ('plain', TweetTextOnly),
        ('reaction_tweet', TweetReaction),
        ('with_link', TweetLink),
        ('retweet', TweetRetweet)
    ])
    def test_tweet_type(self, tweet_test_data_factory, tweet_type, expected_class):
        t, tweet_info = tweet_test_data_factory(tweet_type)
        assert isinstance(t, expected_class)

    @pytest.mark.parametrize("media_type,expected_class", [
        ('media', MediaImage),
    ])
    def test_media_type(self, tweet_test_data_factory, media_type, expected_class):
        t, tweet_info = tweet_test_data_factory(media_type)
        assert isinstance(t.media, expected_class)

class TestUser:
    all_handles = [
        "Marlene_beadles",
        "the_english_way"
    ]

    @pytest.mark.parametrize("user_handle", all_handles)
    def test_user(self, raw_html_user_initial_page_factory, user_collection, user_handle):
        user_info = user_collection[user_handle]
        raw_user = raw_html_user_initial_page_factory(user_handle)
        user = user_factory(raw_user)

        for field, value in user_info._asdict().items():
            # It would be rather complicated to keep some test fixtures values
            # accurate (e.g. number of likes, retweets, ...) so for most
            # of them, the expected values are not set on purpose and therefore
            # not tested
            if value is not None:
                assert value == getattr(user, field)
