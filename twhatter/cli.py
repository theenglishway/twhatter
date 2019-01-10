#!/usr/bin/env python
# coding: utf-8

"""Console script for twhatter."""
import click
import IPython

from twhatter.client import ClientTimeline
from twhatter.output import Database, Tweet


@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)


@main.command()
@click.option('-l', '--limit', type=int, default=100, show_default=True)
@click.argument('user')
def timeline(limit, user):
    """Get some user's Tweets"""
    timeline = ClientTimeline(user)

    for n, t in enumerate(timeline):
        if n >= limit:
            break

        click.echo(t)


@main.group()
@click.option('-d', '--db_url', type=str, default="sqlite:////tmp/db.sqlite3", show_default=True)
@click.pass_context
def db(ctx, db_url):
    ctx.obj['db'] = Database(db_url)


@db.command()
@click.option('-l', '--limit', type=int, default=100, show_default=True)
@click.argument('user')
@click.pass_context
def timeline(ctx, limit, user):
    """Push user's Tweets into a database"""
    timeline = ClientTimeline(user)

    tweets = [
        Tweet.from_raw(t) for n, t in enumerate(timeline) if n < limit
    ]
    ctx.obj['db'].add_all(*tweets)


@db.command()
@click.pass_context
def shell(ctx):
    session = ctx.obj['db'].start()
    user_ns = {
        'db': ctx.obj['db'],
        'session': session,
        'Tweet': Tweet
    }
    IPython.start_ipython(argv=[], user_ns=user_ns)
    ctx.obj['db'].stop(session)


if __name__ == "__main__":
    main(obj={})
