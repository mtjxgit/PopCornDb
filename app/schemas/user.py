from pydantic import BaseModel

class User(BaseModel):
    username: str
    name:str
    disabled: bool | None = None

class CreateUser(BaseModel):
    username:str
    hashed_password:str

class UserInDB(User):
    hashed_password: str