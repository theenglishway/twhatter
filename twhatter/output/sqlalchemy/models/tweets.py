from dataclasses import asdict

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from twhatter.output.sqlalchemy.db import Base


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    username = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comments_nb = Column(Integer)
    retweets_nb = Column(Integer)
    likes_nb = Column(Integer)
    timestamp = Column(DateTime)
    permalink = Column(String)
    text = Column(String)
    _hashtag_list = Column("hashtag_list", String)
    _mention_list = Column("mention_list", String)

    link_to = Column(String)

    retweeter = Column(String)
    retweet_id = Column(Integer)

    reacted_id = Column(Integer)
    reacted_user_id = Column(Integer)

    user = relationship('User', backref='tweets')
    #media = relationship('Media', backref='tweets')

    @hybrid_property
    def hashtag_list(self):
        return self._hashtag_list.split(',') if self._hashtag_list else []

    @hashtag_list.setter
    def hashtag_list(self, values_list):
        self._hashtag_list = ','.join(values_list)

    @hashtag_list.expression
    def hashtag_list(cls):
        return cls._hashtag_list

    @hybrid_property
    def mention_list(self):
        if self._mention_list:
            return [int(user_id) for user_id in self._mention_list.split(',')]
        else:
            return []

    @mention_list.setter
    def mention_list(self, values_list):
        self._mention_list = ','.join([str(v) for v in values_list])

    @mention_list.expression
    def mention_list(cls):
        return cls._mention_list

    def __repr__(self):
        return "<{0} (id={1.id})".format(self.__class__.__qualname__, self)

    @classmethod
    def from_raw(cls, raw_tweet):
        kwargs = {
            k: v
            for k, v in asdict(raw_tweet).items()
            if k not in ['soup', 'media']
        }
        return cls(**kwargs)
