from .base import OutputBase


class Print(OutputBase):
    def output_tweets(self, tweets):
        for t in tweets:
            print(t)

    def output_users(self, users):
        for u in users:
            print(u)
