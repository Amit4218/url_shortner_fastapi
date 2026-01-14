from typing import Union

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    status: int
    message: str
    data: Union[dict | None] = None


class LoginResponseSchema(BaseModel):
    status: int
    message: str
    data: Union[dict | None] = None
    access_token: Union[str | None] = None
    token_type: Union[str | None] = None
