from http import HTTPStatus

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fast_api.database import get_session
from fast_api.models.models import User
from fast_api.schemas.user_schemas import UserIn, UserList, UserOut

app = FastAPI(title='Meu primeiro CRUD sozinho')

router = APIRouter(prefix='/users')

users_db = []


@app.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_user(limit: int = 10, offset: int = 0, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def get_user_id(phone: str, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.phone == phone))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return db_user


app.include_router(router)


@app.post('/', status_code=HTTPStatus.CREATED, response_model=UserOut)
def create_user(user: UserIn, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username)
            | (User.email == user.email)
            | (User.phone == user.phone)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exists',
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
            )
        elif db_user.phone == user.phone:
            raise HTTPException(
                detail='Phone already exists', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        username=user.username,
        phone=user.phone,
        email=user.email,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def update_user(phone: str, user: UserIn, session=Depends(get_session)):
    response = session.scalar(select(User).where(User.phone == phone))

    if not response:
        raise HTTPException(
            detail='User Not Found', status_code=HTTPStatus.NOT_FOUND
        )

    try:
        response.username = user.username
        response.email = user.email
        response.password = user.password
        response.phone = user.phone

        session.add(response)
        session.commit()
        session.refresh(response)

        return response
    except IntegrityError:
        raise HTTPException(
            detail='Username or Email already exists',
            status_code=HTTPStatus.CONFLICT,
        )


@app.delete('/{phone}', status_code=HTTPStatus.OK)
def delete_user(phone: str, session=Depends(get_session)):
    response = session.scalar(select(User).where(User.phone == phone))

    if not response:
        raise HTTPException(
            detail='User Not Found', status_code=HTTPStatus.NOT_FOUND
        )

    session.delete(response)
    session.commit()

    return {'message': 'User Deleted'}
