#!/usr/bin/env python3
from typing import Annotated

from erdi8 import Erdi8
from fastapi import Body, Depends, FastAPI, HTTPException
from functools import lru_cache

from fasterid.schema import ErrorModel, IdModel, RequestModel
from fasterid.settings import Settings, get_settings
from fasterid.store import FileStore, DatabaseStore
from fasterid.database import engine
from fasterid.models import Base

Base.metadata.create_all(bind=engine)

settings = get_settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()

store = FileStore(settings.fasterid_filename)
if settings.use_database:
    store = DatabaseStore(settings.sqlalchemy_database_url)

@app.post(
    "/",
    status_code=201,
    responses={201: {"model": IdModel}, 500: {"model": ErrorModel}},
)
async def id_generator(
    settings: Annotated[Settings, Depends(get_settings)],
    request: RequestModel | None = None,
):
    if request is None:
        request = RequestModel()

    old = e8.increment_fancy(settings.erdi8_start, settings.erdi8_stride)
    last_erdi8 = store.get_last_erdi8(request.prefix)
    if last_erdi8 is not None:
        old = last_erdi8
    else:
        store.create_prefix(request.prefix, old)

    id_list = []
    prefix = request.prefix if request.prefix is not None else ""
    for _ in range(request.number):
        if old == settings.erdi8_start:
            raise HTTPException(500, detail="🤷 ran out of identifiers")
        try:
            new = e8.increment_fancy(old, settings.erdi8_stride)
            id_list.append(f"{prefix}{new}")
            old = new
        except Exception as e:
            raise HTTPException(500, detail=getattr(e, "message", repr(e)))

    if request.key is None:
        store.update_last_erdi8(new, request.prefix)
        return {"id": id_list}

    id_map = {}
    for key in request.key:
        if old == settings.erdi8_start:
            raise HTTPException(500, detail="🤷 ran out of identifiers")
        try:
            mapped_erdi8 = store.get_mapped_erdi8(key, request.prefix)
            if mapped_erdi8 is None:
                new = e8.increment_fancy(old, settings.erdi8_stride)
                id_map[key] = f"{prefix}{new}"
                store.create_mapped_erdi8(key, id_map[key], request.prefix)
                old = new
            else:
                id_map[key] = mapped_erdi8
        except Exception as e:
            raise HTTPException(500, detail=getattr(e, "message", repr(e)))

    store.update_last_erdi8(new, request.prefix)

    return {"id": id_list, "map": id_map}
