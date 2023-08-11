from pydantic import BaseModel, Field
from fasterid.settings import get_settings

settings = get_settings()
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
    key: list[str] | None = Field(
        default=[],
        title="The keys that need to be mapped to identifiers",
    )


class IdModel(BaseModel):
    id: list


class ErrorModel(BaseModel):
    detail: str
