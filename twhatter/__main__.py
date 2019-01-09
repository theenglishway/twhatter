from twhatter.old_query import query_tweets_from_user
from twhatter.query import Query
from twhatter.api import ApiUser
from bs4 import BeautifulSoup
from twhatter.parser import TweetList
from twhatter.output import Print


q = Query(ApiUser("the_english_way").init_page)
soup = BeautifulSoup(q.text, "lxml")
t_list = TweetList(soup)
for t in t_list:
    Print(t)()
