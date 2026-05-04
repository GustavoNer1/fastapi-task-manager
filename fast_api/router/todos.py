from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database import get_session
from fast_api.models.models import Todo, User
from fast_api.schemas.user_schemas import (
    TodoPublic,
    TodoSchema,
    FilterTodo,
    TodoList
)
from fast_api.security import get_current_user
from sqlalchemy import select

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
async def create_todo(todo: TodoSchema, session: Session, user: CurrentUser):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo



@router.get('/', response_model=TodoList)
async def get_todos(
    session: Session, 
    user: CurrentUser,
    todo_filter: Annotated[FilterTodo, Query()]
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(Todo.description.contains(todo_filter.description))

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(query.limit(todo_filter.limit).offset(todo_filter.offset))
    return todos