from typing import List

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    name: str
    phone: str
    email: EmailStr
    city: str | None = None
    state: str | None = None
    age: int


class UserIn(UserOut):
    password: str


class UserList(BaseModel):
    users: List[UserOut]
