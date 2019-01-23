========
Twhatter
========

A simple Python scraper for Twitter.

Motivation
----------

Twitter's API `terms and conditions <https://developer.twitter.com/en/developer-terms/agreement-and-policy.html>`_
have become very demanding in May 2018. Inspired by other attempts, I have
put together yet another twitter scraper that uses a simple HTTP client instead
of the developer API, and allows retrieving any data that can be accessed in an
anonymous browsing session.

This is mostly an attempt for me to produce some clean, functional and
maintainable Python code. I have especially focused on a clean separation
between data retrieval, Twitter pages exploration, and output, which allows
to easily define and combine various crawling strategies and data formats.

And why that terrible name ? Simple, "WHAT's going on TWITTER ?" => TWHATTER !

Features
--------

At the moment, this utility only provides a command-line to interact with it.

Anonymous client
****************

- Get any user's full timeline.
- Get any user's profile data.

Data output
***********

All scraped information can either be :

* displayed on the terminal,
* stored into a JSON / YAML file
* stored into a local database.

Installation
------------

Installation requires Python >= 3.6. ::

    $ pip install --user git+https://code.theenglishway.eu/theenglishway-corp/twhatter

You then have to ensure that `~/.local/bin` is in your `$PATH` or call
`~/.local/bin/twhatter` instead of `twhatter` in the following examples

Usage
-----

Display some user's tweets ::

    $ twhatter timeline realDonaldTrump --limit 40
    <TweetTextOnly (id=1083404900862545920, date=2019-01-10 16:47:11, likes=32033, likes=11087, likes=6935)>
    <TweetTextOnly (id=1083358775925460992, date=2019-01-10 13:43:54, likes=96565, likes=22596, likes=26802)>
    <TweetTextOnly (id=1083358611315789826, date=2019-01-10 13:43:15, likes=52849, likes=9344, likes=9571)>
    <TweetTextOnly (id=1083358150214979585, date=2019-01-10 13:41:25, likes=48808, likes=11096, likes=11499)>
    <TweetTextOnly (id=1083356326833602561, date=2019-01-10 13:34:10, likes=50695, likes=11743, likes=11045)>
    ...
    <TweetTextOnly (id=1083353895030702080, date=2019-01-10 13:24:30, likes=85184, likes=19686, likes=27751)>
    <TweetRetweet (id=1083121283645272064, date=2019-01-09 22:00:12, likes=42640, likes=13189, likes=10242)>
    <TweetRetweet (id=1082774275390693376, date=2019-01-08 23:01:18, likes=52776, likes=14459, likes=2403)>
    <TweetRetweet (id=1083049664021233664, date=2019-01-09 17:15:36, likes=64770, likes=21099, likes=7818)>
    <TweetRetweet (id=1083148367184781312, date=2019-01-09 23:47:49, likes=75514, likes=21966, likes=6145)>

Display their profile information ::

    $ twhatter profile realDonaldTrump
    User(id=25073877, fullname='Donald J. Trump', join_date=datetime.datetime(2009, 3, 18, 0, 0), tweets_nb=40183, following_nb=45, followers_nb=57144827, likes_nb=7)

Put them into a JSON/YAML file ::

    $ twhatter json timeline realDonaldTrump
    $ twhatter yaml profile realDonaldTrump

Put them into a local database (by default in /tmp/db.sqlite) ::

    $ twhatter db timeline realDonaldTrump

Open a session on the local database and make queries with SQLAlchemy ::

    $ twhatter db shell

    In [1]: session.query(Tweet).all()
    Out[1]:
    [<Tweet (id=1020561192849412096),
     <Tweet (id=1021305708908818433),
     <Tweet (id=1024699386528505856),
     <Tweet (id=1026373195790802949),
     <Tweet (id=1026482814164844544),
     <Tweet (id=1027797734613504001)]

In all cases the help is here ::

    $ twhatter --help


Tests
-----

Unit tests are provided. From the root directory in a freshly-cloned repository
and with a clean virtual environment, they can be run with ::

    $ pytest

Useful links
------------

* `Raymond Hettinger's excellent talk about Python 3.7's Dataclasses <https://www.youtube.com/watch?v=T-TwcmT6Rcw>`_

Other scrapers that might fit your needs
****************************************

In Python :

* `twint <https://github.com/twintproject/twint>`_
* `twitterscraper <https://github.com/taspinar/twitterscraper>`_
* `twitter-scraper <https://github.com/kennethreitz/twitter-scraper>`_

In Javascript:

* `scrape-twitter <https://github.com/sebinsua/scrape-twitter>`_
