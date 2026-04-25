from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr


class UserOut(BaseModel):
    username: str
    phone: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserIn(UserOut):
    password: str


class UserList(BaseModel):
    users: List[UserOut]
