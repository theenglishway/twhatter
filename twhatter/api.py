

class Api():
    pass


class ApiUser(Api):
    def __init__(self, user):
        self.user = user

    @property
    def init_page(self):
        return 'https://twitter.com/{}'.format(self.user)
