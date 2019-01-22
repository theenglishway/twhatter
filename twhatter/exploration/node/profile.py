import logging
from .base import NodeBase
from twhatter.client import ClientProfile


class NodeProfile(NodeBase):
    def __init__(self, user):
        super().__init__()
        self.client = ClientProfile(user)

    def __iter__(self):
        super().__iter__()
        yield self.client.user
