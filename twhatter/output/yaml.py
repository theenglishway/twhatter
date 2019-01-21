import yaml
import logging
from bs4 import PageElement

from .base import OutputBase
from twhatter.client import ClientTimeline, ClientProfile


logger = logging.getLogger(__name__)


def PageElement_representer(dumper, data):
    return dumper.represent_data(None)


yaml.add_multi_representer(PageElement, PageElement_representer)


class Yaml(OutputBase):
    def __init__(self, yaml_path):
        logger.info("Output set to {}".format(yaml_path))
        self.yaml_path = yaml_path

    def output_tweets(self, user, limit):
        client_timeline = ClientTimeline(user, limit)

        with open(self.yaml_path, 'w') as f:
            yaml.dump([t for t in client_timeline], f, indent=2)

    def output_user(self, user):
        p = ClientProfile(user)

        with open(self.yaml_path, 'w') as f:
            yaml.dump(p.user, f, indent=2, default_flow_style=False)
