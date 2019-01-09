import requests
from random import choice


class Api():
    pass


class ApiUser(Api):
    HEADERS_LIST = [
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
        'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
    ]

    def __init__(self, user):
        self.user = user

    @property
    def init_page(self):
        return requests.get(
            'https://twitter.com/{}'.format(self.user),
            headers={'User-Agent': choice(self.HEADERS_LIST)}
        )

    @property
    def tweets_from(self, position):
        return (
            "https://twitter.com/i/profiles/show/{u}"
            "/timeline"
            "/tweets"
            "?include_available_features=1"
            "&include_entities=1"
            "&max_position={pos}"
            "&reset_error_state=false"
        )
