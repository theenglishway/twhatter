import json
import logging
from datetime import datetime
from bs4 import PageElement

from .base import OutputBase


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
        self.all_objects = []

    def output_tweets(self, tweets):
        self.all_objects += tweets

    def output_users(self, users):
        self.all_objects += users

    def stop(self):
        with open(self.json_path, 'w') as f:
            json.dump([o for o in self.all_objects], f, cls=TweeterEncoder, indent=4)
