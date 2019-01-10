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

        lines = result.output.split('\n')[:-1]
        assert len(lines) == 100

        for l in lines:
            assert "Tweet" in l

    @pytest.mark.send_request
    def test_timeline_limit(self, cli_runner, user_prolific, tweet_limit):
        result = cli_runner.invoke(
            cli.main,
            ['timeline', user_prolific, '--limit', tweet_limit]
        )
        assert result.exit_code == 0

        lines = result.output.split('\n')[:-1]
        assert len(lines) == tweet_limit

    @pytest.mark.send_request
    def test_profile(self, cli_runner, user_prolific, tweet_limit):
        result = cli_runner.invoke(
            cli.main,
            ['profile', user_prolific]
        )
        assert result.exit_code == 0


class TestDb:
    @pytest.mark.send_request
    def test_timeline_no_limit(self, cli_runner, user_prolific):
        result = cli_runner.invoke(
            cli.main,
            ['db', 'timeline', user_prolific]
        )
        assert result.exit_code == 0

    @pytest.mark.send_request
    def test_timeline_limit(self, cli_runner, user_prolific, tweet_limit):
        result = cli_runner.invoke(
            cli.main,
            ['db', 'timeline', user_prolific, '--limit', tweet_limit]
        )
        assert result.exit_code == 0
