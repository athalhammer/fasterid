import os
from abc import ABC, abstractmethod
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class IdentifierLog(Base):
    __tablename__ = 'identifier_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class IdentifierStore(ABC):
    @abstractmethod
    def get_last_identifier(self) -> str:
        pass

    @abstractmethod
    def store_identifier(self, identifier: str):
        pass


class DatabaseIdentifierStore(IdentifierStore):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_last_identifier(self) -> str:
        session = self.Session()
        try:
            last_entry = session.query(IdentifierLog).order_by(IdentifierLog.id.desc()).first()
            return last_entry.identifier if last_entry else ""
        finally:
            session.close()

    def store_identifier(self, identifier: str):
        session = self.Session()
        try:
            log_entry = IdentifierLog(identifier=identifier, timestamp=datetime.utcnow().isoformat())
            session.add(log_entry)
            session.commit()
        finally:
            session.close()

class LatestOnlyIdentifierStore(IdentifierStore):

    def __init__(self, filename: str):
        self.filename = filename

    def get_last_identifier(self) -> str:
        try:
            with open(self.filename, "r", encoding="ascii") as f:
                return f.readline().strip().split(",")[0]
        except FileNotFoundError:
            return ""

    def store_identifier(self, identifier: str):
        with open(self.filename, "w", encoding="ascii") as f:
            f.write(f"{identifier},{datetime.utcnow().isoformat()}\n")


class FullLogIdentifierStore(IdentifierStore):
    def __init__(self, filename: str):
        self.filename = filename

    def get_last_identifier(self) -> str:
        try:
            with open(self.filename, "r", encoding="ascii") as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()
                buffer = bytearray()
                for i in range(file_size - 1, -1, -1):
                    f.seek(i)
                    char = f.read(1)
                    if char == "\n" and buffer:
                        break
                    buffer.append(ord(char))
                last_line = buffer[::-1].decode("ascii").strip()
                return last_line.strip().split(",")[0]
        except FileNotFoundError:
            return ""

    def store_identifier(self, identifier: str):
        with open(self.filename, "a", encoding="ascii") as f:
            f.write(f"{identifier},{datetime.utcnow().isoformat()}\n")
