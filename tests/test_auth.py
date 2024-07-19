from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_bad_request(client, user):
    response_bad_email = client.post(
        '/auth/token',
        data={'username': 'bad_email', 'password': user.clean_password},
    )

    response_bad_password = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'bad_password'},
    )

    assert response_bad_email.status_code == HTTPStatus.BAD_REQUEST
    assert response_bad_password.status_code == HTTPStatus.BAD_REQUEST
