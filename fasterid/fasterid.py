#!/usr/bin/env python3
from typing import Annotated

from erdi8 import Erdi8
from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fasterid import models
from fasterid.schema import ErrorModel, IdModel, RequestModel
from fasterid.crud import (create_new_mapped_erdi8, create_new_prefix,
                           get_last_erdi8, get_mapped_erdi8, update_last_erdi8)
from fasterid.database import SessionLocal, engine
from fasterid.settings import Settings, get_settings

models.Base.metadata.create_all(bind=engine)

settings = get_settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/",
    status_code=201,
    responses={201: {"model": IdModel}, 500: {"model": ErrorModel}},
)
async def id_generator(
    settings: Annotated[Settings, Depends(get_settings)],
    request: Annotated[RequestModel, Body(embed=True)] | None = None,
    db: Session = Depends(get_db),
):
    if request is None:
        request = RequestModel()

    old = e8.increment_fancy(settings.erdi8_start, settings.erdi8_stride)
    db_prefix = get_last_erdi8(db, request.prefix)
    if db_prefix is not None:
        old = db_prefix.last_erdi8
    else:
        db_prefix = create_new_prefix(db, request.prefix, old)

    id_list = []
    for _ in range(request.number):
        if old == settings.erdi8_start:
            raise HTTPException(500, detail="🤷 ran out of identifiers")
        try:
            new = e8.increment_fancy(old, settings.erdi8_stride)
            id_list.append(f"{request.prefix}{new}")
            old = new
        except Exception as e:
            raise HTTPException(500, detail=getattr(e, "message", repr(e)))

    if request.key is None:
        update_last_erdi8(db, db_prefix, new)
        return {"id": id_list}

    id_map = {}
    for key in request.key:
        if old == settings.erdi8_start:
            raise HTTPException(500, detail="🤷 ran out of identifiers")
        try:
            db_erdi8 = get_mapped_erdi8(db, db_prefix, key)
            if db_erdi8 is None:
                new = e8.increment_fancy(old, settings.erdi8_stride)
                id_map[key] = f"{request.prefix}{new}"
                create_new_mapped_erdi8(db, db_prefix, key, id_map[key])
                old = new
            else:
                id_map[key] = db_erdi8.erdi8
        except Exception as e:
            raise HTTPException(500, detail=getattr(e, "message", repr(e)))

    update_last_erdi8(db, db_prefix, new)

    return {"id": id_list, "map": id_map}