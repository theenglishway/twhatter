from twhatter.parser import TweetList, Tweet


class TestTweetList:
    def test_len(self, raw_html_user_initial_page):
        t_list = TweetList(raw_html_user_initial_page)
        assert len(t_list) == 20

    def test_iter(self, raw_html_user_initial_page):
        t_list = TweetList(raw_html_user_initial_page)
        for t in t_list:
            assert isinstance(t, Tweet)
