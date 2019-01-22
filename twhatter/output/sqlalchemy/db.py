import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from twhatter.output import OutputBase


# Registry of SQLAlchemy's models
class_registry = {}
# Base class for SQLAlchemy models
Base = declarative_base(class_registry=class_registry)

# Session maker
Session = scoped_session(sessionmaker(autoflush=False))

logger = logging.getLogger(__name__)


class Database(OutputBase):
    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.session_maker = Session
        self.session_maker.configure(bind=engine)
        Base.metadata.create_all(engine)

    def start(self):
        self.session = self.session_maker()
        self.all_objs = []
        return self.session

    def _add_no_fail(self, session, obj):
        # This is an extremely unefficient way to add objects to the database,
        # but the only way I've found so far to deal with duplications
        session.add(obj)
        try:
            session.commit()
            return 1
        except IntegrityError as e:
            logger.debug("Error on commit : {}".format(e))
            session.rollback()
            return 0

    def output_tweets(self, tweets):
        Tweet = class_registry['Tweet']
        logger.info("Adding {} tweets".format(len(tweets)))

        self.all_objs += [Tweet.from_raw(t) for t in tweets]
        #self.session.add_all([Tweet.from_raw(t) for t in tweets])

    def output_users(self, users):
        User = class_registry['User']
        logger.info("Adding {} tweets".format(len(users)))

        self.all_objs += [User.from_raw(t) for t in users]
        #self.session.add_all([User.from_raw(u) for u in users])

    def stop(self):
        for o in self.all_objs:
            self._add_no_fail(self.session, o)
        #self.session.commit()
        self.session.close()
