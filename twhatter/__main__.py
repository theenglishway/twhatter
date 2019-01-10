from twhatter.api import ApiUser
from twhatter.output import Print


user = "the_english_way"
a = ApiUser(user)

for t in a.iter_tweets():
    Print(t)()
