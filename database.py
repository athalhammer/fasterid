from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings

settings = settings.Settings()

if settings.fasterid_filename is not None:
    database_url = f"sqlite:///./{settings.fasterid_filename}"
else:
    database_url = settings.sqlalchemy_database_url
engine = create_engine(database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
