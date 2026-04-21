from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api.app import app


def test_get_user_return_message():
    """
    Este teste tem 3 etapas (AAA)
    A: Arrange - arranjo
    A: Act - executa a coisa (SUT)
    A: Assert - Garata que A é A
    """
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
