import json
import logging
from datetime import datetime
from bs4 import PageElement

from .base import OutputBase
from twhatter.client import ClientTimeline, ClientProfile


logger = logging.getLogger(__name__)


class TweeterEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%c %z")

        if isinstance(o, PageElement):
            return None

        return o.__dict__


class Json(OutputBase):
    def __init__(self, json_path):
        logger.info("Output set to {}".format(json_path))
        self.json_path = json_path

    def output_tweets(self, user, limit):
        client_timeline = ClientTimeline(user, limit)

        with open(self.json_path, 'w') as f:
            json.dump([t for t in client_timeline], f, cls=TweeterEncoder, indent=4)

    def output_user(self, user):
        p = ClientProfile(user)

        with open(self.json_path, 'w') as f:
            json.dump(p.user, f, cls=TweeterEncoder, indent=4)
