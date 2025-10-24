from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator

Base = declarative_base()

class DatabaseSession:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=True)
        self.session_maker = sessionmaker(
            self.engine, class_=Session, expire_on_commit=False
        )

    def get_session(self) -> Generator[Session, None, None]:
        session = self.session_maker()
        try:
            yield session
        finally:
            session.close()

    def close(self):
        self.engine.dispose()