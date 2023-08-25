from pathlib import Path
from abc import ABC

from fasterid.crud import (create_db_mapped_erdi8, create_db_prefix,
                           get_db_mapped_erdi8, get_db_prefix,
                           update_last_erdi8_db_prefix)

class Store(ABC):

    def get_last_erdi8(self, prefix: str = None) -> str | None:
        pass

    def update_last_erdi8(self, erdi8: str, prefix: str = None):
        pass

    def create_mapped_erdi8(self, key: str, erdi8: str, prefix: str = None):
        pass

    def get_mapped_erdi8(self, key: str, prefix: str = None) -> str | None:
        pass

    def create_prefix(self, prefix: str, erdi8: str):
        pass

class FileStore(Store):
    def __init__(self, filename):
        self.fasterid_filename = filename
        Path(filename).touch(exist_ok=True)

    def get_last_erdi8(self, prefix: str = None) -> str | None:
        with open(self.fasterid_filename, "r+") as f:
            file_content = f.readline().strip()
            if file_content != "":
                return file_content
            return None

    def update_last_erdi8(self, erdi8: str, prefix: str = None):
        with open(self.fasterid_filename, "r+") as f:
            f.seek(0)
            print(erdi8, file=f)

    def create_mapped_erdi8(self, key: str, erdi8: str, prefix: str = None):
        pass

    def get_mapped_erdi8(self, key: str, prefix: str = None) -> str | None:
        return None

    def create_prefix(self, prefix: str, erdi8: str):
        pass


class DatabaseStore(Store):
    def __init__(self, database_url):
        self.database_url = database_url
        # TODO: fix below
        # if settings.sqlalchemy_database_url is None:
        #     database_url = f"sqlite:///./{settings.fasterid_filename}"
        # else:
        #     database_url = settings.sqlalchemy_database_url
        # engine = create_engine(database_url, connect_args={"check_same_thread": False})
        # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Base = declarative_base()
        
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_last_erdi8(self, prefix: str = None) -> str | None:
        db = self.get_db()
        db_prefix = get_db_prefix(db, prefix)
        return db_prefix.last_erdi8

    def update_last_erdi8(self, erdi8: str, prefix: str = None):
        db = self.get_db()
        db_prefix = get_db_prefix(db, prefix)
        update_last_erdi8_db_prefix(db, db_prefix, erdi8)

    def create_mapped_erdi8(self, key: str, erdi8: str, prefix: str = None):
        db = self.get_db()
        db_prefix = get_db_prefix(db, prefix)
        create_db_mapped_erdi8(db, db_prefix, key, erdi8)

    def get_mapped_erdi8(self, key: str, prefix: str = None) -> str | None:
        db = self.get_db()
        db_prefix = get_db_prefix(db, prefix)
        return get_db_mapped_erdi8(db, db_prefix)

    def create_prefix(self, prefix: str, erdi8: str):
        db = self.get_db()
        create_db_prefix(
            db,
            prefix,
        )
