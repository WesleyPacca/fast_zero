from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'username': 'John Doe', 'email': 'jhon@batata.com', 'id': 1}
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Bob',
            'email': 'bon@batata.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Bob',
        'email': 'bon@batata.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/3',
        json={
            'username': 'Bob',
            'email': 'bon@batata.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Bob',
        'email': 'bon@batata.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    response = client.get('/user/3')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delet_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delet_user_not_found(client):
    response = client.delete('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND
