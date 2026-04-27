from http import HTTPStatus

from fast_api.schemas.user_schemas import UserOut


def test_create_user(client):
    payload = {
        'username': 'guguinha guguinha',
        'phone': '11911110030',
        'email': 'guguinha.guguinha@email.com',
        'password': 'senhaSegura',
    }

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'guguinha guguinha',
        'phone': '11911110030',
        'email': 'guguinha.guguinha@email.com',
    }


def test_get_user_return_message(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_with_user(client, user, token):
    user_db = UserOut.model_validate(user).model_dump()
    response = client.get(
        '/users', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_db]}


def test_get_user_phone(client, user, token):
    user_db = UserOut.model_validate(user).model_dump()
    response = client.get(
        f'/users/{user.phone}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_db


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.phone}',headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Felipe Toledo',
            'phone': '11911110100',
            'email': 'felipe.aguiar@email.com',
            'password': 'senhaSegura',
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Felipe Toledo',
        'phone': '11911110100',
        'email': 'felipe.aguiar@email.com',
    }


def test_delete(client, user):
    response = client.delete(f'/users/{user.phone}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'acess_token' in token
