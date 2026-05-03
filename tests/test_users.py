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
        f'/users/{user.phone}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_delete(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.phone}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.phone}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
            'phone': '11911110110',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
