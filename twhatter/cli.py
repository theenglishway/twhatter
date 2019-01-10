#!/usr/bin/env python
# coding: utf-8

"""Console script for twhatter."""
import click

from twhatter.api import ApiUser


@click.group()
@click.option('-l', '--limit', type=int, default=100, show_default=True)
@click.pass_context
def main(ctx, limit):
    ctx.ensure_object(dict)

    ctx.obj['limit'] = limit


@main.command()
@click.argument('user')
@click.pass_context
def own(ctx, user):
    """Get some user's Tweets"""
    a = ApiUser(user)

    for n, t in enumerate(a.iter_tweets()):
        if n >= ctx.obj['limit']:
            break

        click.echo(t)
            break

        click.echo(t)


if __name__ == "__main__":
    main(obj={})
