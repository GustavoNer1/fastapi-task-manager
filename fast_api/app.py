from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_api.schemas.user_schemas import UserIn, UserList, UserOut

app = FastAPI(title='Meu primeiro CRUD sozinho')

users_db = [
    # {
    #     'name': 'Gustavo Neri',
    #     'phone': '11970299205',
    #     'email': 'gustavoneri448@gmail.com',
    #     'password': '123456789',
    #     'city': 'Jundiai',
    #     'state': 'SP',
    #     'age': 24,
    # },
    # {
    #     'name': 'Camila Souza',
    #     'phone': '11988887777',
    #     'email': 'camila.souza@email.com',
    #     'password': 'senha123',
    #     'city': 'null',
    #     'state': 'SP',
    #     'age': 31,
    # },
    # {
    #     'name': 'Lucas Andrade',
    #     'phone': '11955554444',
    #     'email': 'lucas.andrade@email.com',
    #     'password': 'abc123456',
    #     'city': 'Campinas',
    #     'state': 'null',
    #     'age': 28,
    # },
    # {
    #     'name': 'Mariana Costa',
    #     'phone': '11933332222',
    #     'email': 'mariana.costa@email.com',
    #     'password': 'minhasenha',
    #     'city': 'null',
    #     'state': 'null',
    #     'age': 35,
    # },
    # {
    #     'name': 'Felipe Rocha',
    #     'phone': '11911110000',
    #     'email': 'felipe.rocha@email.com',
    #     'password': 'senhaSegura',
    #     'city': 'São Paulo',
    #     'state': 'SP',
    #     'age': 27,
    # },
]


@app.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_user():
    return {'users': users_db}


@app.get('/users/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def get_user_id(phone: str):
    response = next(
        (user for user in users_db if user['phone'] == phone), None
    )

    if response is None:
        raise HTTPException(status_code=404, detail='User not found')

    return response


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserOut)
def create_user(user: UserIn):
    response = user.model_dump()
    users_db.append(response)
    return response


@app.put('/users/{phone}', status_code=HTTPStatus.OK, response_model=UserOut)
def update_user(phone: str, user: UserIn):
    response = next(
        (user for user in users_db if user['phone'] == phone), None
    )

    if response is None:
        raise HTTPException(status_code=404, detail='User not found')

    update_user = user.model_dump()
    update_user['phone'] = phone

    index = users_db.index(response)
    users_db[index] = update_user
    return update_user


@app.delete(
    '/users/{phone}', status_code=HTTPStatus.OK, response_model=UserOut
)
def delete_user(phone: str):
    response = next(
        (user for user in users_db if user['phone'] == phone), None
    )

    if response is None:
        raise HTTPException(status_code=404, detail='User not found')

    index = users_db.index(response)
    return users_db.pop(index)
