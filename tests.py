

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
