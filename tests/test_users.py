from http import HTTPStatus

from app.schemas.user_schema import UserCreate

def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'JonasL',
            'email': 'jonaszin@gmail.com',
            'password': 'admin12',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
            'username': 'JonasL',
            'email': 'jonaszin@gmail.com',
            'password': 'admin12',
        }