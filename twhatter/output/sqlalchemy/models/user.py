from dataclasses import asdict

from sqlalchemy import Column, Integer, String, DateTime

from twhatter.output.sqlalchemy.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    join_date = Column(DateTime)
    tweets_nb = Column(Integer)
    following_nb = Column(Integer)
    followers_nb = Column(Integer)
    likes_nb = Column(Integer)

    def __repr__(self):
        return "<{0} (id={1.id})".format(self.__class__.__qualname__, self)

    @classmethod
    def from_raw(cls, raw_user):
        kwargs = {
            k: v
            for k, v in asdict(raw_user).items()
        }
        return cls(**kwargs)
