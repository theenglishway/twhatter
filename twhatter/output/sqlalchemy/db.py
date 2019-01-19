import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError


# Base class for SQLAlchemy models
Base = declarative_base()

# Session maker
Session = scoped_session(sessionmaker(autoflush=False))

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.session_maker = Session
        self.session_maker.configure(bind=engine)
        Base.metadata.create_all(engine)

    def start(self):
        return self.session_maker()

    def stop(self, session):
        session.close()

    def add_all(self, *objs):
        logger.info("Adding {} objects".format(len(objs)))
        session = self.session_maker()

        unique_errors = 0
        # This is an extremely unefficient way to add objects to the database,
        # but the only way I've found so far to deal with duplications
        for o in objs:
            session.add(o)
            try:
                session.commit()
            except IntegrityError as e:
                logger.debug("Error on commit : {}".format(e))
                unique_errors += 1
                session.rollback()

        if unique_errors:
            logger.info(
                "{} objects were already in the database".format(unique_errors)
            )

        session.close()
