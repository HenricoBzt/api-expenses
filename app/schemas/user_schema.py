from pydantic import BaseModel, EmailStr, ConfigDict

class UserPublic(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserPublic):
    password: str


class UserList(BaseModel):
    users: list[UserPublic]

class Token(BaseModel):
    access_token: str
    token_type: str