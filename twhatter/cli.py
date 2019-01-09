#!/usr/bin/env python
# coding: utf-8

"""Console script for twhatter."""
import click

from twhatter.api import ApiUser


@click.group()
def main():
    pass


@main.command()
@click.argument('user')
def own(user):
    """Get all the user's own publications"""
    a = ApiUser(user)

    for t in a.iter_tweets():
        click.echo(t)

if __name__ == "__main__":
    main()
