from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from fasterid.settings import get_settings

settings = get_settings()
if settings.sqlalchemy_database_url is None:
    database_url = f"sqlite:///./{settings.fasterid_filename}"
else:
    database_url = settings.sqlalchemy_database_url
engine = create_engine(database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
