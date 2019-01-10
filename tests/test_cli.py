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


class TestOwn:
    @pytest.mark.send_request
    def test_no_limit(self, cli_runner, user):
        result = cli_runner.invoke(cli.main, ['own', user])
        assert result.exit_code == 0

        lines = result.output.split('\n')[:-1]
        assert 100 > len(lines) > 0

        for l in lines:
            assert "Tweet" in l

    @pytest.mark.send_request
    def test_limit(self, cli_runner, user, tweet_limit):
        result = cli_runner.invoke(cli.main, ['--limit', tweet_limit, 'own', user])
        assert result.exit_code == 0

        lines = result.output.split('\n')[:-1]
        assert len(lines) == tweet_limit


class TestDb:
    @pytest.mark.send_request
    def test_no_limit(self, cli_runner, user):
        result = cli_runner.invoke(cli.main, ['db', 'own', user])
        assert result.exit_code == 0
