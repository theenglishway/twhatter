# coding: utf-8

"""Console script for twhatter."""
import sys
import click

from twhatter.query import Query
from twhatter.api import ApiUser
from bs4 import BeautifulSoup
from twhatter.parser import TweetList
from twhatter.output import Print

@click.command()
@click.option('--user', prompt='User name to check',
              help='The person to greet.')
def main(user):
    """Console script for twhatter."""
    q = Query(ApiUser(user).init_page)
    soup = BeautifulSoup(q.text, "lxml")
    t_list = TweetList(soup)
    for t in t_list:
        click.echo(t)


if __name__ == "__main__":
    main()
