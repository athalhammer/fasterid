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

    # this also implies that we skip the very first identifier if the store is empty
    old = identifier_store.get_last_identifier() or settings.erdi8_start
    id_list = []
    is_ld_json = "ld+json" in accept or settings.fasterid_always_rdf
    mime = "application/ld+json" if is_ld_json else "application/json"
    ts_prop = settings.fasterid_ts_property if is_ld_json else settings.fasterid_ts

    for _ in range(request.number):
        next_id = e8.increment_fancy(old, settings.erdi8_stride)
        if next_id == settings.erdi8_stop:
            break
        ts = datetime.now().astimezone()
        dic = {"@id": f"{next_id}", ts_prop: ts.isoformat()}
        if is_ld_json:
            dic["@id"] = f"{request.prefix}{next_id}"
            dic[settings.fasterid_id_property] = next_id
        id_list.append(dic)
        old = next_id

    if not id_list:
        raise HTTPException(500, detail="🤷 ran out of identifiers")

    for dic in id_list:
        identifier_store.store_identifier(
            dic["@id"].split("/")[-1], datetime.fromisoformat(dic[ts_prop])
        )

    logger.info(id_list)
    if len(id_list) == 1:
        return JSONResponse(content=id_list[0], media_type=mime, status_code=201)
    return JSONResponse(content=id_list, media_type=mime, status_code=201)
