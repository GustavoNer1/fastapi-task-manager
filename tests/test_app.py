from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api.app import app, users_db


def reset_users_db():
    users_db.clear()


def test_create_user():
    reset_users_db()
    client = TestClient(app)

    payload = {
        'name': 'Felipe Rocha',
        'phone': '11911110000',
        'email': 'felipe.rocha@email.com',
        'password': 'senhaSegura',
        'city': 'São Paulo',
        'state': 'SP',
        'age': 27,
    }

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'Felipe Rocha',
        'phone': '11911110000',
        'email': 'felipe.rocha@email.com',
        'city': 'São Paulo',
        'state': 'SP',
        'age': 27,
    }


def test_get_user_return_message():
    reset_users_db()
    client = TestClient(app)

    client.post(
        '/users',
        json={
            'name': 'Felipe Rocha',
            'phone': '11911110000',
            'email': 'felipe.rocha@email.com',
            'password': 'senhaSegura',
            'city': 'São Paulo',
            'state': 'SP',
            'age': 27,
        },
    )

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'name': 'Felipe Rocha',
                'phone': '11911110000',
                'email': 'felipe.rocha@email.com',
                'city': 'São Paulo',
                'state': 'SP',
                'age': 27,
            }
        ]
    }


def test_update_user():
    reset_users_db()
    client = TestClient(app)

    client.post(
        '/users',
        json={
            'name': 'Felipe Rocha',
            'phone': '11911110000',
            'email': 'felipe.rocha@email.com',
            'password': 'senhaSegura',
            'city': 'São Paulo',
            'state': 'SP',
            'age': 27,
        },
    )

    payload = {
        'name': 'Gustavo Alencar',
        'phone': '11911110000',
        'email': 'alencar.rocha@email.com',
        'password': 'segurançasenha',
        'city': 'Campinas',
        'state': 'SP',
        'age': 24,
    }

    response = client.put('/users/11911110000', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Gustavo Alencar',
        'phone': '11911110000',
        'email': 'alencar.rocha@email.com',
        'city': 'Campinas',
        'state': 'SP',
        'age': 24,
    }


def test_delete():
    reset_users_db()
    client = TestClient(app)

    client.post(
        '/users',
        json={
            'name': 'Gustavo Alencar',
            'phone': '11911110000',
            'email': 'alencar.rocha@email.com',
            'password': 'segurançasenha',
            'city': 'Campinas',
            'state': 'SP',
            'age': 24,
        },
    )

    response = client.delete('/users/11911110000')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Gustavo Alencar',
        'phone': '11911110000',
        'email': 'alencar.rocha@email.com',
        'city': 'Campinas',
        'state': 'SP',
        'age': 24,
    }
