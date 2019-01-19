#!/usr/bin/env python
# coding: utf-8

"""Console script for twhatter."""
import click
import IPython

from twhatter.client import ClientTimeline, ClientProfile
from twhatter.output import Print
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
    ctx.obj['stdout'] = Print()


@main.command()
@click.option('-l', '--limit', type=int, default=100, show_default=True)
@click.argument('user')
@click.pass_context
def timeline(ctx, limit, user):
    """Get some user's Tweets"""
    ctx.obj['stdout'].output_tweets(user, limit)


@main.command()
@click.argument('user')
@click.pass_context
def profile(ctx, user):
    """Get basic info about some user"""
    ctx.obj['stdout'].output_user(user)


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
    ctx.obj['db'].output_tweets(user, limit)


@db.command()
@click.argument('user')
@click.pass_context
def profile(ctx, user):
    """Push some user into a database"""
    ctx.obj['db'].output_user(user)


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
