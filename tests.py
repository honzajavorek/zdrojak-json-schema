

import json
import pytest


@pytest.fixture
def test_client():
    from web import app
    app.config['TESTING'] = True
    return app.test_client()


def test_send_data(test_client):
    data_in = {'name': 'Honza', 'age': 42}
    response = test_client.post('/users', data=json.dumps(data_in),
                                content_type='application/json')
    assert response.status_code == 201

    data_out = json.loads(response.data)
    assert data_out['id']
    assert data_out['name'] == data_in['name']
    assert data_out['age'] == data_in['age']


def test_invalid_data(test_client):
    data_in = {'id': 2, 'name': 'Honza',
               'age': 'Life, the Universe and Everything'}
    response = test_client.post('/users', data=json.dumps(data_in),
                                content_type='application/json')
    assert response.status_code == 400

    data_out = json.loads(response.data)
    assert len(data_out['errors']) == 2


def test_send_address(test_client):
    data_in = {'name': 'Honza',
               'address': {'country': 'Czech Republic', 'city': 'Krno'}}
    response = test_client.post('/users', data=json.dumps(data_in),
                                content_type='application/json')
    assert response.status_code == 201

    data_out = json.loads(response.data)
    assert data_out['id']
    assert data_out['name'] == data_in['name']
    assert data_out['address'] == data_in['address']


def test_invalid_address(test_client):
    data_in = {'name': 'Honza',
               'address': {'city': 'Krno', 'number': '11', 'mayor': 'Rumun'}}
    response = test_client.post('/users', data=json.dumps(data_in),
                                content_type='application/json')
    assert response.status_code == 400

    data_out = json.loads(response.data)
    assert len(data_out['errors']) == 3
