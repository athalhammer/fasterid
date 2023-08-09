from sqlalchemy.orm import Session

import models
# import settings
# from erdi8 import Erdi8

# settings = settings.Settings()
# e8 = Erdi8(settings.erdi8_safe)

def get_mapped_erdi8(db: Session, prefix: str, key: str):
    return db.query(models.Erdi8).filter(models.Erdi8.key == key).first()

def get_mapped_erdi8s(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Erdi8).offset(skip).limit(limit).all()

def get_last_erdi8(db: Session, prefix: str):
    return db.query(models.Prefix).filter(models.Prefix.prefix == prefix).first()

def update_last_erdi8(db: Session, db_prefix: models.Prefix, erdi8: str):
    # Update the last erdi8 for this prefix
    db_prefix.last_erdi8 = erdi8
    db.commit()
    db.refresh(db_prefix)
    return db_prefix

def create_new_prefix(db: Session, prefix: str | None, erdi8: str):
    db_prefix = models.Prefix(prefix=prefix, last_erdi8 = erdi8)
    db.add(db_prefix)
    db.commit()
    db.refresh(db_prefix)
    return db_prefix

