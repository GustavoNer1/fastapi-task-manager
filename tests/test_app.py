from http import HTTPStatus

from fast_api.app import users_db
from fast_api.schemas.user_schemas import UserOut


def reset_users_db():
    users_db.clear()


def test_create_user(client):
    # reset_users_db()
    # client = TestClient(app)

    payload = {
        'username': 'Felipe Rocha',
        'phone': '11911110000',
        'email': 'felipe.rocha@email.com',
        'password': 'senhaSegura',
    }

    response = client.post('/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Felipe Rocha',
        'phone': '11911110000',
        'email': 'felipe.rocha@email.com',
    }


def test_get_user_return_message(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_with_user(client, user):
    user_db = UserOut.model_validate(user).model_dump()
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_db]}


def test_get_user_phone(client, user):
    user_db = UserOut.model_validate(user).model_dump()
    response = client.get(f'/{user.phone}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_db


def test_update_user(client, user):
    response = client.put(
        f'/{user.phone}',
        json={
            'username': 'Felipe Toledo',
            'phone': '11911110100',
            'email': 'felipe.aguiar@email.com',
            'password': 'senhaSegura',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Felipe Toledo',
        'phone': '11911110100',
        'email': 'felipe.aguiar@email.com',
    }


def test_delete(client, user):
    response = client.delete(f'/{user.phone}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}
