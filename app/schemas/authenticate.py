"""
Module containing Pydantic BaseModel classes for authentication-related data schemas.
"""
from pydantic import BaseModel
from fastapi import Form

class SignUp(BaseModel):
    """
    Represents a sign-up form data schema.
    """
    name: str
    username: str
    password: str

    @classmethod
    def as_form(cls, name: str = Form(...), username: str = Form(...), password: str = Form(...)):
        """
        Converts form data into SignUp instance.
        """
        return cls(name=name, username=username, password=password)

class Login(BaseModel):
    """
    Represents a login form data schema.
    """
    username: str
    password: str

    @classmethod
    def as_login_form(cls, username: str = Form(...), password: str = Form(...)):
        """
        Converts form data into Login instance.
        """
        return cls(username=username, password=password)

class Token(BaseModel):
    """
    Represents a token schema.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Represents token data schema.
    """
    username: str | None = None
