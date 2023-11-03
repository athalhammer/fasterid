#!/usr/bin/env python3

from pathlib import Path
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, BaseSettings, Field
from erdi8 import Erdi8


class Settings(BaseSettings):
    erdi8_stride: int
    erdi8_start: str
    erdi8_safe: bool
    fasterid_max_num: int
    fasterid_max_prefix_len: int
    fasterid_filename: str

    class Config:
        env_file = "fasterid.env"


settings = Settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()

Path(settings.fasterid_filename).touch(exist_ok=True)


class RequestModel(BaseModel):
    prefix: str | None = Field(
        default="",
        title="The prefix to be added to the erdi8 string",
        max_length=settings.fasterid_max_prefix_len,
    )
    number: int | None = Field(
        default=1,
        title="The number of identifiers that need to be generated",
        lt=settings.fasterid_max_num + 1,
    )


class IdModel(BaseModel):
    id: str = Field(..., alias="@id")


class ErrorModel(BaseModel):
    detail: str


@app.post(
    "/",
    status_code=201,
    responses={201: {"model": List[IdModel] | IdModel}, 500: {"model": ErrorModel}},
)
async def id_generator(
    request: Annotated[RequestModel, Body(embed=True)] | None = None
):
    if request is None:
        request = RequestModel()

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
                id_list.append({"@id": f"{request.prefix}{new}"})
                old = new
            except Exception as e:
                raise HTTPException(500, detail=getattr(e, "message", repr(e)))
        f.seek(0)
        print(new, file=f)
        if len(id_list) == 1:
            return id_list[0]
        return id_list
