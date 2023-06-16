#!/usr/bin/env python3

from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, BaseSettings, Field
from erdi8 import Erdi8

class RequestModel(BaseModel):
    prefix: str | None  = Field(
        default="", title="The prefix to be added to the erdi8 string", max_length=300
    )
    number: int | None = Field(
        default=1, title="The number of identifiers that need to be generated", lt=50
    )

class IdModel(BaseModel):
    id: list

class ErrorModel(BaseModel):
    detail: str


class Settings(BaseSettings):
    erdi8_stride: int
    erdi8_start: str
    erdi8_safe: bool
    erdi8_filename: str

    class Config:
        env_file = "fasterid.env"


settings = Settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()

Path(settings.erdi8_filename).touch(exist_ok=True)


@app.post(
    "/",
    status_code=201,
    responses={201: {"model": IdModel}, 500: {"model": ErrorModel}}
)
async def id_generator(request: Annotated[RequestModel, Body(embed=True)] | None = None) -> IdModel:
    if request is None:
        request = RequestModel()
    old = settings.erdi8_start
    with open(settings.erdi8_filename, "r+") as f:
        tmp = f.readline().strip()
        if tmp != "":
            old = tmp
        if tmp == settings.erdi8_start:
            raise HTTPException(500, detail="🤷 ran out of identifiers")
        else:
            l = []
            for _ in range(request.number):
                try:
                    new = e8.increment_fancy(old, settings.erdi8_stride)
                    l.append(f"{request.prefix}{new}")
                    old = new
                except Exception as e:
                    raise HTTPException(500, detail=getattr(e, "message", repr(e)))
                f.seek(0)
                print(new, file=f)
            return {"id": l}
