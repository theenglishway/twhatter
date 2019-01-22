#!/usr/bin/env python
# coding: utf-8

"""Console script for twhatter."""
import click
import IPython

from twhatter.output import Print, Json, Database, Yaml
from twhatter.output.sqlalchemy import Tweet, User
from twhatter.log import log_setup
from twhatter.exploration import StrategyDumb, NodeTimeline, NodeProfile


@click.group()
@click.option('-v', '--verbosity',
              type=click.Choice(['none', 'info', 'debug', 'verbose']),
              default='info', show_default=True)
@click.pass_context
def main(ctx, verbosity):
    log_setup(verbosity)
    ctx.ensure_object(dict)
    ctx.obj['output'] = Print()


@main.group()
@click.option('-d', '--db_url', type=str, default="sqlite:////tmp/db.sqlite3", show_default=True)
@click.pass_context
def db(ctx, db_url):
    ctx.obj['output'] = Database(db_url)


@main.group()
@click.option('-f', '--json_file', type=str, default="/tmp/output.json", show_default=True)
@click.pass_context
def json(ctx, json_file):
    ctx.obj['output'] = Json(json_file)


@main.group()
@click.option('-f', '--yaml_file', type=str, default="/tmp/output.yaml", show_default=True)
@click.pass_context
def yaml(ctx, yaml_file):
    ctx.obj['output'] = Yaml(yaml_file)


@main.command()
@click.option('-l', '--limit', type=int, default=100, show_default=True)
@click.argument('user')
@click.pass_context
def timeline(ctx, limit, user):
    """Get some user's Tweets"""
    start_node = NodeTimeline(user, limit)
    strategy = StrategyDumb(start_node)
    strategy(ctx.obj['output'])

@main.command()
@click.argument('user')
@click.pass_context
def profile(ctx, user):
    """Get basic info about some user"""
    start_node = NodeProfile(user)
    strategy = StrategyDumb(start_node)
    strategy(ctx.obj['output'])


@db.command()
@click.pass_context
def shell(ctx):
    session = ctx.obj['output'].start()
    user_ns = {
        'db': ctx.obj['output'],
        'session': session,
        'Tweet': Tweet,
        'User': User
    }
    IPython.start_ipython(argv=[], user_ns=user_ns)
    ctx.obj['output'].stop(session)


db.add_command(profile)
db.add_command(timeline)

json.add_command(profile)
json.add_command(timeline)

yaml.add_command(profile)
yaml.add_command(timeline)

if __name__ == "__main__":
    main(obj={})
