from .base import OutputBase
from twhatter.client import ClientTimeline, ClientProfile


class Print(OutputBase):
    def output_tweets(self, user, limit):
        client_timeline = ClientTimeline(user, limit)

        for t in client_timeline:
            print(t)

    def output_user(self, user):
        p = ClientProfile(user)
        print(p.user)
