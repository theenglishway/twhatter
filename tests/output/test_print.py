import pytest
from twhatter.output import Print

@pytest.fixture
def timeline_attribute():
    return "twhatter.output.print.ClientTimeline"

@pytest.fixture
def profile_attribute():
    return "twhatter.output.print.ClientProfile"

@pytest.fixture
def output():
    return Print()

@pytest.mark.parametrize("fixtures_file, expected_len", [
    ('tests/fixtures/tweets/text_only_10.yaml', 10),
    ('tests/fixtures/tweets/retweet_10.yaml', 10),
    ('tests/fixtures/tweets/link_10.yaml', 10),
    ('tests/fixtures/tweets/reaction_9.yaml', 9),
])
def test_output_tweets(capsys, timeline_mock_factory, output, fixtures_file, expected_len):
    timeline_mock_factory(fixtures_file)
    output.output_tweets(None, None)

    captured = capsys.readouterr()
    assert len(captured.out.split('\n')) == expected_len + 1
