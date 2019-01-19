#!/usr/bin/env python
# coding: utf-8

"""Console script for twhatter."""
import click
import IPython

from twhatter.client import ClientTimeline, ClientProfile
from twhatter.output.sqlalchemy import Database, Tweet, User
from twhatter.log import log_setup


@click.group()
@click.option('-v', '--verbosity',
              type=click.Choice(['none', 'info', 'debug', 'verbose']),
              default='info', show_default=True)
@click.pass_context
def main(ctx, verbosity):
    log_setup(verbosity)
    ctx.ensure_object(dict)


@main.command()
@click.option('-l', '--limit', type=int, default=100, show_default=True)
@click.argument('user')
def timeline(limit, user):
    """Get some user's Tweets"""
    timeline = ClientTimeline(user, limit)

    for t in timeline:
        click.echo(t)


@main.command()
@click.argument('user')
def profile(user):
    """Get basic info about some user"""
    p = ClientProfile(user)
    click.echo(p.user)


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
    timeline = ClientTimeline(user, limit)

    tweets = [
        Tweet.from_raw(t) for n, t in enumerate(timeline) if n < limit
    ]
    profiles = set()
    for t in timeline:
        p = ClientProfile(t.screen_name)
        profiles.add(p)
    users = [User.from_raw(p.user) for p in profiles]
    ctx.obj['db'].add_all(*users, *tweets)


@db.command()
@click.argument('user')
@click.pass_context
def profile(ctx, user):
    """Push some user into a database"""
    p = ClientProfile(user)

    ctx.obj['db'].add_all(User.from_raw(p.user))


@db.command()
@click.pass_context
def shell(ctx):
    session = ctx.obj['db'].start()
    user_ns = {
        'db': ctx.obj['db'],
        'session': session,
        'Tweet': Tweet,
        'User': User
    }
    IPython.start_ipython(argv=[], user_ns=user_ns)
    ctx.obj['db'].stop(session)


if __name__ == "__main__":
    main(obj={})
