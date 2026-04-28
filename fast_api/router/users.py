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
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models.models import User
from fast_api.schemas.user_schemas import (
    FilterPage,
    UserIn,
    UserList,
    UserOut,
)
from fast_api.security import get_current_user, get_password_hash

# Cria a aplicação principal FastAPI.
# Esse objeto representa sua API.
app = FastAPI(title='Meu primeiro CRUD sozinho')

# Cria um grupo de rotas com prefixo /users.
# Todas as rotas abaixo ficarão dentro de /users.
router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


# Lista usuários com paginação simples.
# Exemplo:
# GET /users/?limit=10&offset=0
@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):
    # Monta e executa uma consulta:
    # SELECT * FROM users LIMIT :limit OFFSET :offset
    users = list(
        session.scalars(
            select(User).limit(filter_users.limit).offset(filter_users.offset)
        )
    )

    # Retorna no formato esperado pelo UserList:
    # {"users": [...]}
    return {'users': users}


# Busca um usuário pelo telefone.
# Exemplo:
# GET /users/11999999999
@router.get('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def get_user_by_phone(
    phone: str,
    session: Session,
    current_user: CurrentUser,
):
    # Busca o primeiro usuário cujo telefone seja igual ao parâmetro da URL.
    db_user = session.scalar(select(User).where(User.phone == phone))

    # Se não encontrar, retorna erro 404.
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    # Retorna o objeto ORM.
    # O response_model=UserOut filtra a resposta e remove a senha.
    return db_user


# Cria um novo usuário.
# Exemplo:
# POST /users/
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserOut)
def create_user(
    user: UserIn,
    session: Session,
):
    # Verifica se já existe usuário com mesmo username, email ou phone.
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username)
            | (User.email == user.email)
            | (User.phone == user.phone)
        )
    )

    # Se encontrou algum conflito, retorna uma mensagem específica.
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

    # Cria uma instância do model SQLAlchemy.
    # UserIn é schema de entrada.
    # User é model de banco.
    db_user = User(
        username=user.username,
        phone=user.phone,
        email=user.email,
        password=get_password_hash(user.password),
    )

    # Adiciona o objeto na sessão.
    session.add(db_user)

    # Confirma a transação e salva no banco.
    session.commit()

    # Atualiza o objeto com dados gerados pelo banco.
    # Exemplo: id, created_at, updated_at.
    session.refresh(db_user)

    # Retorna o usuário criado.
    # UserOut remove password da resposta.
    return db_user


# Atualiza um usuário existente pelo telefone.
# Exemplo:
# PUT /users/11999999999
@router.put('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def update_user(
    phone: str,
    user: UserIn,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.phone != phone:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    try:
        # Atualiza os campos do objeto encontrado.
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        current_user.phone = user.phone

        # Confirma as alterações.
        session.commit()

        # Atualiza o objeto com os dados mais recentes do banco.
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        # Depois de erro de integridade, a sessão precisa de rollback.
        session.rollback()

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username, email or phone already exists',
        )


# Remove um usuário pelo telefone.
# Exemplo:
# DELETE /users/11999999999
@router.delete('/{phone}', status_code=HTTPStatus.OK)
def delete_user(
    phone: str,
    session: Session,
    current_user: CurrentUser,
):

    if current_user.phone != phone:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    # Marca o objeto para remoção.
    session.delete(current_user)

    # Confirma a exclusão no banco.
    session.commit()

    return {'message': 'User Deleted'}


# Inclui o grupo de rotas /users na aplicação principal.
app.include_router(router)
