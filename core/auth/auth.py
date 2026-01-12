from fastapi import HTTPException

from schemas import LoginUserSchema, RegisterUserSchema


def login_user(user: LoginUserSchema):
    """authenticates the user with an jwt token after the appropriate validation and checking"""

    # check if the data is correct

    if (user.email == "") or (user.password == ""):
        raise HTTPException(404, "Both feilds must be filled!")

    # check if the user is in the database

    # check if the password is correct

    # if correct generate jwt token

    # return the jwt token to the user

    pass


def register_user(user: RegisterUserSchema):
    """registers / saves the user in the db the appropriate validation and checking"""
    pass
