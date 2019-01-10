#!/usr/bin/env python
# coding: utf-8

"""Console script for twhatter."""
import click

from twhatter.api import ApiUser


@click.group()
def main():
    pass


@main.command()
@click.option('-l', '--limit', type=int, default=100, show_default=True)
@click.argument('user')
def own(user, limit):
    """Get some user's Tweets"""
    a = ApiUser(user)

    for n, t in enumerate(a.iter_tweets()):
        if n >= limit:
            break

        click.echo(t)


if __name__ == "__main__":
    main()
