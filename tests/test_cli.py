#!/usr/bin/env python
# coding: utf-8

"""Tests for `twhatter` package."""
import pytest

from twhatter import cli


def test_command_line_interface(cli_runner):
    """Test the CLI."""
    result = cli_runner.invoke(cli.main)
    assert result.exit_code == 0

    help_result = cli_runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


class TestMain:
    @pytest.mark.send_request
    def test_timeline_no_limit(self, cli_runner, user_prolific):
        result = cli_runner.invoke(
            cli.main,
            ['timeline', user_prolific]
        )
        assert result.exit_code == 0

        # Remove log lines
        lines = [
            l for l in result.output.split('\n')[:-1] if "twhatter" not in l
        ]
        assert len(lines) == 101

        for l in lines[:-1]:
            assert "Tweet" in l

        assert "User" in lines[-1]

    @pytest.mark.xfail
    @pytest.mark.send_request
    @pytest.mark.parametrize("tweet_limit", [
        10,
        30
    ])
    def test_timeline_limit(self, cli_runner, user_prolific, tweet_limit):
        result = cli_runner.invoke(
            cli.main,
            ['timeline', user_prolific, '--limit', tweet_limit]
        )
        assert result.exit_code == 0

        # Remove log lines
        lines = [
            l for l in result.output.split('\n')[:-1] if "twhatter" not in l
        ]
        assert len(lines) == tweet_limit + 1

    @pytest.mark.send_request
    def test_profile(self, cli_runner, user_prolific):
        result = cli_runner.invoke(
            cli.main,
            ['profile', user_prolific]
        )
        assert result.exit_code == 0


@pytest.mark.xfail
class TestDb:
    @pytest.mark.send_request
    def test_timeline_no_limit(self, cli_runner, user_prolific):
        result = cli_runner.invoke(
            cli.main,
            ['db', 'timeline', user_prolific]
        )
        assert result.exit_code == 0

    @pytest.mark.send_request
    @pytest.mark.parametrize("tweet_limit", [
        10,
        30
    ])
    def test_timeline_limit(self, cli_runner, user_prolific, tweet_limit):
        result = cli_runner.invoke(
            cli.main,
            ['db', 'timeline', user_prolific, '--limit', tweet_limit]
        )
        assert result.exit_code == 0
