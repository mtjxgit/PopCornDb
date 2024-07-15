from pydantic import BaseModel
from fastapi import Form

class signup(BaseModel): 
    name:str
    username:str
    password:str
    @classmethod
    def as_form(cls,name:str=Form(...), username:str = Form(...),password:str=Form(...)):
        return cls(name =name ,username = username,password = password)
    
class login(BaseModel):
    username:str
    password:str
    @classmethod
    def as_login_form(cls,username:str = Form(...),password:str=Form(...)):
        return cls(username = username,password = password)

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
