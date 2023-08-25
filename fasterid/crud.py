from sqlalchemy import insert
from sqlalchemy.orm import Session

from fasterid import models


def get_db_prefix(db: Session, prefix: str | None) -> models.Prefix:
    return db.query(models.Prefix).filter(models.Prefix.prefix == prefix).first()

def create_db_prefix(db: Session, prefix: str | None, erdi8: str):
    db_prefix = models.Prefix(prefix=prefix, last_erdi8=erdi8)
    db.add(db_prefix)
    db.commit()
    db.refresh(db_prefix)
    return db_prefix


def update_last_erdi8_db_prefix(db: Session, db_prefix: models.Prefix, erdi8: str):
    # Update the last erdi8 for this prefix
    db_prefix.last_erdi8 = erdi8
    db.commit()
    db.refresh(db_prefix)
    return db_prefix


def get_db_mapped_erdi8(
    db: Session, db_prefix: models.Prefix, key: str
) -> models.Erdi8:
    return (
        db.query(models.Erdi8)
        .filter(models.Erdi8.key == key, models.Erdi8.prefix_id == db_prefix.id)
        .first()
    )


def get_db_mapped_erdi8s(
    db: Session, db_prefix: models.Prefix, key: list[str]
) -> list[models.Erdi8]:
    return (
        db.query(models.Erdi8)
        .filter(models.Erdi8.key == key, models.Erdi8.prefix_id == db_prefix.id)
        .all()
    )


def create_db_mapped_erdi8(db: Session, db_prefix: models.Prefix, key: str, erdi8: str):
    db_erdi8 = models.Erdi8(prefix_id=db_prefix.id, key=key, erdi8=erdi8)
    db.add(db_erdi8)
    db.commit()
    db.refresh(db_erdi8)
    return db_erdi8


def create_db_mapped_erdi8s(db: Session, prefix: str | None, map: dict[str, str]):
    db_prefix = get_db_prefix(db, prefix)

    data = []
    for key, erdi8 in map.items():
        data.append({"prefix_id": db_prefix.id, "key": key, "erdi8": erdi8})

    db_results = db.execute(insert(models.Erdi8), data)

    return db_results
