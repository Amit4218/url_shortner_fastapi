from typing import Dict, Union

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    status: int
    message: str
    data: Union[Dict | None] = None


class ErrorResponseSchema(BaseModel):
    status: int
    error: str
    message: str
