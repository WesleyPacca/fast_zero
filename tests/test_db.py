from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='Wesley', password='teste1', email='teste@teste')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Wesley'))

    assert user.username == 'Wesley'
