import yaml
import logging
from bs4 import PageElement

from .base import OutputBase


logger = logging.getLogger(__name__)


def PageElement_representer(dumper, data):
    return dumper.represent_data(None)


yaml.add_multi_representer(PageElement, PageElement_representer)


class Yaml(OutputBase):
    def __init__(self, yaml_path):
        logger.info("Output set to {}".format(yaml_path))
        self.yaml_path = yaml_path
        self.all_objects = []

    def output_tweets(self, tweets):
        self.all_objects += tweets

    def output_users(self, users):
        self.all_objects += users

    def stop(self):
        with open(self.yaml_path, 'w') as f:
            yaml.dump([u for u in self.all_objects], f, indent=2, default_flow_style=False)
