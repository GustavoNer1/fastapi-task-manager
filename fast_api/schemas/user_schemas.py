from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fast_api.models.models import TodoState


class UserBase(BaseModel):
    username: str
    phone: str
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserOut]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    limit: int = Field(ge=0, default=10)
    offset: int = Field(ge=0, default=0)


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=4)
    description: str | None = None
    state: TodoState | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState = Field(default=TodoState.todo)


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]