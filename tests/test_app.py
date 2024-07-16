from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_creat_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'John Doe',
            'email': 'jhon@batata.com',
            'password': 'batata123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'John Doe',
        'email': 'jhon@batata.com',
        'id': 1,
    }


def test_creat_user_username_already_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'Teste',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_creat_user_email_already_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'John Doe',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Bob',
            'email': 'bob@batata.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Bob',
        'email': 'bob@batata.com',
        'id': user.id,
    }


def test_update_user_other_user(client, users, token):
    response = client.put(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Bob',
            'email': 'bob@batata.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Teste',
        'email': 'teste@test.com',
        'id': 1,
    }


def test_read_user_not_found(client, user):
    response = client.get('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delet_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delet_user_other_user(client, users, token):
    response = client.delete(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_bad_request(client, user):
    response_bad_email = client.post(
        '/token',
        data={'username': 'bad_email', 'password': user.clean_password},
    )

    response_bad_password = client.post(
        '/token',
        data={'username': user.email, 'password': 'bad_password'},
    )

    assert response_bad_email.status_code == HTTPStatus.BAD_REQUEST
    assert response_bad_password.status_code == HTTPStatus.BAD_REQUEST
