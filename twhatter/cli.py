# coding: utf-8

"""Console script for twhatter."""
import click

from twhatter.api import ApiUser


@click.command()
@click.option('--user', prompt='User name to check',
              help='The person to greet.')
@click.option('-r', '--replies', is_flag=True)
def main(user, replies):
    """Console script for twhatter."""
    a = ApiUser(user)

    for t in a.iter_tweets():
        click.echo(t)

if __name__ == "__main__":
    main()
