#!/usr/bin/env python3

# Copyright (C) 2023  Andreas Thalhammer
# Please get in touch if you plan to use this in a commercial setting.

import logging
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException, Body, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from erdi8 import Erdi8


logger = logging.getLogger("uvicorn.error")

class Settings(BaseSettings):
    erdi8_stride: int
    erdi8_start: str
    erdi8_safe: bool
    fasterid_max_num: int
    fasterid_always_rdf: bool
    fasterid_max_prefix_len: int
    fasterid_filename: str
    fasterid_id_property: str
    fasterid_id_default_prefix: str

    class Config:
        env_file = "fasterid.env"

settings = Settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()

Path(settings.fasterid_filename).touch(exist_ok=True)

class RequestModel(BaseModel):
    prefix: str | None = Field(
        default=settings.fasterid_id_default_prefix,
        title="The prefix to be added to the erdi8 string",
        max_length=settings.fasterid_max_prefix_len,
    )
    number: int | None = Field(
        default=1,
        title="The number of identifiers that need to be generated",
        lt=settings.fasterid_max_num + 1,
    )
    rdf: bool | None = Field(
        default=False,
        title="Flag if RDF should be returned in JSON-LD format. If true the prefix combined with the identifier needs to form a valid IRI",
    )

@app.post("/")
async def id_generator(request: RequestModel | None = None):
    if request is None:
        request = RequestModel()
    mime = "application/json"
    old = e8.increment_fancy(settings.erdi8_start, settings.erdi8_stride)
    with open(settings.fasterid_filename, "r+", encoding="ascii") as f:
        file_content = f.readline().strip()
        if file_content != "":
            old = file_content

        id_list = []
        for _ in range(request.number):
            if old == settings.erdi8_start:
                raise HTTPException(500, detail="🤷 ran out of identifiers")
            try:
                new = e8.increment_fancy(old, settings.erdi8_stride)
                dic = {"@id": f"{request.prefix}{new}"}
                if request.rdf or settings.fasterid_always_rdf:
                    mime = "application/ld+json"
                    dic[settings.fasterid_id_property] = new
                id_list.append(dic)
                old = new
            except Exception as e:
                raise HTTPException(500, detail=getattr(e, "message", repr(e)))
        f.seek(0)
        print(new, file=f)
        logger.info(id_list)
        if len(id_list) == 1:
            return JSONResponse(content=id_list[0], media_type=mime, status_code=201)
        return JSONResponse(content=id_list, media_type=mime, status_code=201)
