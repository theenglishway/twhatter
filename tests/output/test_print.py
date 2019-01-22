import pytest
from twhatter.output import Print


@pytest.fixture
def output():
    return Print()

@pytest.mark.parametrize("fixtures_file, expected_len", [
    ('tests/fixtures/tweets/text_only_10.yaml', 10),
    ('tests/fixtures/tweets/retweet_10.yaml', 10),
    ('tests/fixtures/tweets/link_10.yaml', 10),
    ('tests/fixtures/tweets/reaction_9.yaml', 9),
])
def test_output_tweets(capsys, tweets_factory, output, fixtures_file, expected_len):
    tweets = tweets_factory(fixtures_file)
    output.output_tweets(tweets)

    captured = capsys.readouterr()
    assert len(captured.out.split('\n')) == expected_len + 1
