import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from twhatter.output import OutputBase
from twhatter.client import ClientTimeline, ClientProfile


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
        return self.session_maker()

    def stop(self, session):
        session.close()

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
        client_timeline = ClientTimeline(user, limit)
        Tweet = class_registry['Tweet']
        User = class_registry['User']
        session = self.start()
        tweets = [Tweet.from_raw(t) for t in client_timeline]
        logger.info("Adding {} tweets".format(len(tweets)))

        profiles = set()
        for t in client_timeline:
            p = ClientProfile(t.username)
            profiles.add(p)
        users = [User.from_raw(p.user) for p in profiles]

        unique_errors = 0
        for u in users:
            self._add_no_fail(session, u)
        for t in tweets:
            unique_errors += self._add_no_fail(session, t)

        if unique_errors:
            logger.info(
                "{} tweets were already in the database".format(unique_errors)
            )

        self.stop(session)

    def output_users(self, users):
        User = class_registry['User']
        p = ClientProfile(user)
        session = self.start()

        self._add_no_fail(session, User.from_raw(p.user))
        self.stop(session)
