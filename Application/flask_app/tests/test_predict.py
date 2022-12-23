import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"login" in response.data
    assert b"auth" in response.data

    auth.login()
    response = client.get('/')
    assert b"logout" in response.data

    # add more assert clauses.


@pytest.mark.parametrize('path', (
    '/history',
    '/update'
))
def test_login_required(client, path):
    response = client.post(path)
    assert 1 == 1
