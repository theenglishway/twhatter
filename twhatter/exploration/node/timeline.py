import logging
from .base import NodeBase
from twhatter.client import ClientTimeline


class NodeTimeline(NodeBase):
    def __init__(self, user, limit=100):
        super().__init__()
        self.client = ClientTimeline(user, limit)

    def __iter__(self):
        super().__iter__()
        yield from self.client
