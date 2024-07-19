from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token_invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_payload_incorrect(client, user):
    data = {'test': 'test'}
    token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_current_user_not_user_in_db(client, user):
    data = {'sub': 'bad_username'}
    payload = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {payload}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
