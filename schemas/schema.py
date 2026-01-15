from pydantic import BaseModel


class LoginUserSchema(BaseModel):
    email: str
    password: str


class RegisterUserSchema(BaseModel):
    username: str
    email: str
    password: str


class UrlSchema(BaseModel):
    original_url: str
