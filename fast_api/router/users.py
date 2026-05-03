from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    Query,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database import get_session
from fast_api.models.models import User
from fast_api.schemas.user_schemas import (
    FilterPage,
    UserIn,
    UserList,
    UserOut,
)
from fast_api.security import get_current_user, get_password_hash

app = FastAPI(title='Meu primeiro CRUD sozinho')

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def get_users(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):
    users = list(
        await session.scalars(
            select(User).limit(filter_users.limit).offset(filter_users.offset)
        )
    )

    return {'users': users}


@router.get('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
async def get_user_by_phone(
    phone: str,
    session: Session,
    current_user: CurrentUser,
):
    db_user = await session.scalar(select(User).where(User.phone == phone))

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return db_user


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserOut)
async def create_user(
    user: UserIn,
    session: Session,
):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username)
            | (User.email == user.email)
            | (User.phone == user.phone)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )

        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

        if db_user.phone == user.phone:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Phone already exists',
            )

    db_user = User(
        username=user.username,
        phone=user.phone,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.put('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
async def update_user(
    phone: str,
    user: UserIn,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.phone != phone:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        current_user.phone = user.phone

        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username, email or phone already exists',
        )


@router.delete('/{phone}', status_code=HTTPStatus.OK)
async def delete_user(
    phone: str,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.phone != phone:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    await session.commit()

    return {'message': 'User Deleted'}


app.include_router(router)
