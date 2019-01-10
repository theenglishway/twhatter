from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError


# Base class for SQLAlchemy models
Base = declarative_base()

# Session maker
Session = scoped_session(sessionmaker(autoflush=False))


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
        session = self.session_maker()
        session.add_all(objs)
        try:
            session.commit()
        except IntegrityError:
            print("Some objects could not be inserted")
        session.close()
