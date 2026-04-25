from http import HTTPStatus

# HTTPStatus → status como 200, 201, 404
from fastapi import FastAPI, HTTPException

# FastAPI → cria a aplicação
# HTTPException → lança erro HTTP
from fast_api.schemas.user_schemas import UserIn, UserList, UserOut

# UserIn/UserOut/UserList → schemas Pydantic

app = FastAPI(title='Meu primeiro CRUD sozinho', prefix='/users')
# Criando a aplicação
users_db = []
# Lista temporaria/banco de dados temporario


@app.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_user():
    return {'users': users_db}


@app.get('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def get_user_id(phone: str):
    response = next(
        (user for user in users_db if user['phone'] == phone), None
    )
    # Procure dentro da lista users_db
    # o primeiro usuário cujo phone seja igual ao phone da URL.
    # Se não achar, retorne None.

    if response is None:
        raise HTTPException(status_code=404, detail='User not found')

    return response


@app.post('/', status_code=HTTPStatus.CREATED, response_model=UserOut)
def create_user(user: UserIn):
    response = user.model_dump()
    # transforma o objeto Pydantic em dicionário Python.
    users_db.append(response)
    return response


@app.put('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def update_user(phone: str, user: UserIn):
    response = next(
        (user for user in users_db if user['phone'] == phone), None
    )

    if response is None:
        raise HTTPException(status_code=404, detail='User not found')

    update_user = user.model_dump()
    update_user['phone'] = phone
    # Força o telefone ser o mesmo telefone da URL

    index = users_db.index(response)
    users_db[index] = update_user
    return update_user


@app.delete('/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def delete_user(phone: str):
    response = next(
        (user for user in users_db if user['phone'] == phone), None
    )

    if response is None:
        raise HTTPException(status_code=404, detail='User not found')

    index = users_db.index(response)
    return users_db.pop(index)
    # remove da lista
    # retorna o item removido
