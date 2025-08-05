from pydantic import BaseModel, EmailStr, ConfigDict


class UserPublic(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserList(BaseModel):
    users: list[UserPublic]


class UserListMe(BaseModel):
    id: int
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
