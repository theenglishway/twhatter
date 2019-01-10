========
Twhatter
========


A simple scraper for Twitter

Installation
------------

Installation requires Python >= 3.6.

..highlight: shell

    $ pip install --user git+https://code.theenglishway.eu/theenglishway-corp/twhatter

You then have to ensure that `~/.local/bin` in your `$PATH` or call
`~/.local/bin/twhatter` instead of `twhatter` in the following examples

Use
---

Display some user's tweets

..highlight: shell

    $ twhatter timeline realDonaldTrump --limit 10
    <TweetTextOnly (id=1083404900862545920, date=2019-01-10 16:47:11, likes=32033, likes=11087, likes=6935)>
    <TweetTextOnly (id=1083358775925460992, date=2019-01-10 13:43:54, likes=96565, likes=22596, likes=26802)>
    <TweetTextOnly (id=1083358611315789826, date=2019-01-10 13:43:15, likes=52849, likes=9344, likes=9571)>
    <TweetTextOnly (id=1083358150214979585, date=2019-01-10 13:41:25, likes=48808, likes=11096, likes=11499)>
    <TweetTextOnly (id=1083356326833602561, date=2019-01-10 13:34:10, likes=50695, likes=11743, likes=11045)>
    <TweetTextOnly (id=1083353895030702080, date=2019-01-10 13:24:30, likes=85184, likes=19686, likes=27751)>
    <TweetRetweet (id=1083121283645272064, date=2019-01-09 22:00:12, likes=42640, likes=13189, likes=10242)>
    <TweetRetweet (id=1082774275390693376, date=2019-01-08 23:01:18, likes=52776, likes=14459, likes=2403)>
    <TweetRetweet (id=1083049664021233664, date=2019-01-09 17:15:36, likes=64770, likes=21099, likes=7818)>
    <TweetRetweet (id=1083148367184781312, date=2019-01-09 23:47:49, likes=75514, likes=21966, likes=6145)>

Display their profile information

..highlight: shell

    $ twhatter profile realDonaldTrump
    User(id=25073877, screen_name='Donald J. Trump', join_date=datetime.datetime(2009, 3, 18, 0, 0), tweets_nb=40183, following_nb=45, followers_nb=57144827, likes_nb=7)

Put them into a local database (by default in /tmp/db.sqlite)

..highlight: shell

    $ twhatter db timeline realDonaldTrump

Open a session on the local database and make queries with SQLAlchemy

..highlight: shell

    $ twhatter db shell

..highlight: python

    In [1]: session.query(Tweet).all()
    Out[1]:
    [<Tweet (id=1020561192849412096),
     <Tweet (id=1021305708908818433),
     <Tweet (id=1024699386528505856),
     <Tweet (id=1026373195790802949),
     <Tweet (id=1026482814164844544),
     <Tweet (id=1027797734613504001)]
