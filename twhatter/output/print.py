class Print:
    def __init__(self, tweet):
        self.tweet = tweet

    def __call__(self, *args, **kwargs):
        print(self.tweet)
