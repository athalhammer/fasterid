#!/usr/bin/env python3

# Copyright (C) 2023  Andreas Thalhammer
# Please get in touch if you plan to use this in a commercial setting.
from .store import (
    LatestOnlyIdentifierStore,
    FullLogIdentifierStore,
    DatabaseIdentifierStore,
)
from .settings import Settings, StorageType

import logging
from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from erdi8 import Erdi8


logger = logging.getLogger("uvicorn.error")

settings = Settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()


class RequestModel(BaseModel):
    prefix: str | None = Field(
        default=settings.fasterid_default_prefix,
        title="The prefix to be added to the erdi8 string",
        max_length=settings.fasterid_max_prefix_len,
    )
    number: int | None = Field(
        default=1,
        title="The number of identifiers that need to be generated",
        lt=settings.fasterid_max_num + 1,
    )


if settings.fasterid_store_type == StorageType.DATABASE:
    identifier_store = DatabaseIdentifierStore(settings.fasterid_store_loc)
elif settings.fasterid_store_type == StorageType.FILE_LOG:
    identifier_store = FullLogIdentifierStore(settings.fasterid_store_loc)
else:
    identifier_store = LatestOnlyIdentifierStore(settings.fasterid_store_loc)


@app.post(
    "/",
    responses={
        201: {
            "description": "Generated identifiers",
            "content": {
                "application/json": {
                    "example": {
                        "@id": "erdi8",
                        "timestamp": "2023-01-01T00:00:00.000000",
                    }
                },
                "application/ld+json": {
                    "example": {
                        "@id": "https://example.com/erdi8",
                        "https://schema.org/identifier": "erdi8",
                        "https://schema.org/dateCreated": "2023-01-01T00:00:00.000000",
                    }
                },
            },
        }
    },
)
async def id_generator(
    request: RequestModel | None = None, accept: Annotated[str | None, Header()] = None
):
    if request is None:
        request = RequestModel()

    old = identifier_store.get_last_identifier()
    if not old:
        old = e8.increment_fancy(settings.erdi8_start, settings.erdi8_stride)

    id_list = []
    is_ld_json = "ld+json" in accept or settings.fasterid_always_rdf
    mime = "application/ld+json" if is_ld_json else "application/json"
    ts_prop = settings.fasterid_ts_property if is_ld_json else "timestamp"

    for _ in range(request.number):
        if old == settings.erdi8_start:
            raise HTTPException(500, detail="🤷 ran out of identifiers")
        try:
            new = e8.increment_fancy(old, settings.erdi8_stride)
            ts = datetime.utcnow()
            dic = {"@id": f"{request.prefix}{new}", ts_prop: ts.isoformat()}
            if is_ld_json:
                dic[settings.fasterid_id_property] = new
            id_list.append(dic)
            old = new
        except Exception as e:
            raise HTTPException(500, detail=getattr(e, "message", repr(e)))

    for dic in id_list:
        identifier_store.store_identifier(
            dic["@id"].split("/")[-1], datetime.fromisoformat(dic[ts_prop])
        )

    logger.info(id_list)
    if len(id_list) == 1:
        return JSONResponse(content=id_list[0], media_type=mime, status_code=201)
    return JSONResponse(content=id_list, media_type=mime, status_code=201)
