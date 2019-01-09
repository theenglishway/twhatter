from twhatter.api import ApiUser
from bs4 import BeautifulSoup
from twhatter.parser import TweetList
from twhatter.output import Print

user="the_english_way"
a = ApiUser(user)

for t in a.iter_own_tweets():
    Print(t)()

for t in a.iter_all_tweets():
    Print(t)()
