from sqlalchemy.orm import Session
from sqlalchemy import insert
import models

def get_mapped_erdi8(db: Session, db_prefix: models.Prefix, key: str):
    return db.query(models.Erdi8).filter(models.Erdi8.key == key, models.Erdi8.prefix_id == db_prefix.id).first()

def get_mapped_erdi8s(db: Session, db_prefix: models.Prefix, key: list[str]):
    return db.query(models.Erdi8).filter(models.Erdi8.key == key, models.Erdi8.prefix_id == db_prefix.id).all()

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

def create_new_mapped_erdi8(db: Session, db_prefix: models.Prefix, key: str, erdi8: str):
    db_erdi8 = models.Erdi8(prefix_id=db_prefix.id, key=key, erdi8=erdi8)
    db.add(db_erdi8)
    db.commit()
    db.refresh(db_erdi8)
    return db_erdi8

def create_new_mapped_erdi8s(db: Session, prefix: str | None, map: dict[str, str]):
    db_prefix = get_last_erdi8(db, prefix)

    data = []
    for key, erdi8 in map.items():
        data.append({"prefix_id": db_prefix.id, "key": key, "erdi8": erdi8})

    db_results = db.execute(
        insert(models.Erdi8),
        data
    )

    return db_results

# def get_next_erdi8(db: Session, prefix: str):
#     db_prefix = get_last_erdi8(db, prefix)
#     if db_prefix is not None:
#         if db_prefix.last_erdi8 == settings.erdi8_start:
#             raise Exception(detail="🤷 ran out of identifiers")
#         new_erdi8 = e8.increment_fancy(db_prefix.last_erdi8, settings.erdi8_stride)
#         return update_last_erdi8(db, prefix, new_erdi8)
    
#     # If there is no prefix entry, create one and store it
#     return create_new_prefix(db, prefix)

# def get_next_erdi8s(db: Session, prefix: str, number: int = 1):
#     id_list = []
#     for _ in range(number):
#             id_list.append(get_next_erdi8(db, prefix))

#     return id_list

# def create_new_prefix(db: Session, prefix: str):
#     erdi8 = e8.increment_fancy(settings.erdi8_start, settings.erdi8_stride)
#     db_prefix = models.Prefix(prefix=prefix, last_erdi8 = erdi8)
#     db.add(db_prefix)
#     db.commit()
#     db.refresh(db_prefix)
#     return db_prefix

# def create_new_mapped_erdi8(db: Session, prefix: str, key: str):
#     db_prefix = get_next_erdi8(db, prefix)
#     db_erdi8 = models.Erdi8(prefix_id=db_prefix.id, key=key, erdi8=db_prefix.last_erdi8)
#     db.add(db_erdi8)
#     db.commit()
#     db.refresh(db_erdi8)
#     return db_erdi8