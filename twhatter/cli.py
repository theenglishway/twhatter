# coding: utf-8

"""Console script for twhatter."""
import click

from twhatter.api import ApiUser
from bs4 import BeautifulSoup
from twhatter.parser import TweetList


@click.command()
@click.option('--user', prompt='User name to check',
              help='The person to greet.')
def main(user):
    """Console script for twhatter."""
    p = ApiUser(user).init_page
    soup = BeautifulSoup(p.text, "lxml")
    t_list = TweetList(soup)
    for t in t_list:
        click.echo(t)


if __name__ == "__main__":
    main()
