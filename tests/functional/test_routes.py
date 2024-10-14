from iebank_api import app, db
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        db.drop_all()


def test_hello_world(client):
    """
    Test the '/' route to return 'Hello, World!'
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data

def test_skull(client):
    """
    Test the '/skull' route to check database connection info
    """
    response = client.get('/skull')
    assert response.status_code == 200
    assert b'BACKEND SKULL!' in response.data
    assert b'Database URL:' in response.data


def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(client):
    """
    Test the creation of a new account with valid data
    """
    account_data = {
        'name': 'John Doe',
        'currency': '€',
        'country': 'Spain',
        'email': 'jd@gmail.com',
        'type': 'Savings'
    }
    response = client.post('/accounts', json=account_data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['name'] == 'John Doe'
    assert json_data['currency'] == '€'
    assert json_data['country'] == 'Spain'

def test_get_accounts(client):
    """
    Test retrieving all accounts after creating one
    """
    account_data = {
        'name': 'John Doe',
        'currency': '€',
        'country': 'Spain',
        'email': 'jd@gmail.com',
        'type': 'Savings'
    }
    client.post('/accounts', json=account_data)
    
    response = client.get('/accounts')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data['accounts']) == 1
    assert json_data['accounts'][0]['name'] == 'John Doe'

def test_get_single_account(client):
    """
    Test retrieving a single account by its ID
    """
    account_data = {
        'name': 'John Doe',
        'currency': '€',
        'country': 'Spain',
        'email': 'jd@gmail.com',
        'type': 'Savings'
    }
    response = client.post('/accounts', json=account_data)
    account_id = response.get_json()['id']
    
    response = client.get(f'/accounts/{account_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['name'] == 'John Doe'

def test_update_account(client):
    """
    Test updating an existing account
    """
    account_data = {
        'name': 'John Doe',
        'currency': '€',
        'country': 'Spain',
        'email': 'jd@gmail.com',
        'type': 'Savings'
    }
    response = client.post('/accounts', json=account_data)
    account_id = response.get_json()['id']
    
    updated_data = {
        'name': 'Jane Doe',
        'email': 'jane@gmail.com'
    }
    response = client.put(f'/accounts/{account_id}', json=updated_data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['name'] == 'Jane Doe'
    assert json_data['email'] == 'jane@gmail.com'


def test_delete_account(client):
    """
    Test deleting an account
    """
    account_data = {
        'name': 'John Doe',
        'currency': '€',
        'country': 'Spain',
        'email': 'jd@gmail.com',
        'type': 'Savings'
    }
    response = client.post('/accounts', json=account_data)
    account_id = response.get_json()['id']
    
    response = client.delete(f'/accounts/{account_id}')
    assert response.status_code == 200
    
    # Check if the account was actually deleted
    response = client.get(f'/accounts/{account_id}')
    assert response.status_code == 404  # or appropriate status for not found