from iebank_api.models import Account
from iebank_api import app, db
import pytest

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status, country, email, type and created_at fields are defined correctly
    """
    account = Account('John Doe', '€', 'Spain', 'jd@gmail.com', 'Savings')
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'
    assert account.country == 'Spain'
    assert account.email == 'jd@gmail.com'
    assert account.type == 'Savings'

def test_currency():
    """
    GIVEN an Account model
    WHEN a new Account is created with an invalid currency symbol
    THEN check that it raises a ValueError
    """
    
    with pytest.raises(ValueError) as excinfo:
        Account('John Doe', '!', 'Spain', 'jd@gmail.com', 'Savings')

def test_empty_name():
    """
    GIVEN an Account model
    WHEN a new Account is created with an invalid currency symbol
    THEN check that it raises a ValueError
    """
    
    with pytest.raises(ValueError) as excinfo:
        Account('', '$', 'Spain', 'jd@gmail.com', 'Savings')

def test_default_values():
    account = Account(name='John Doe', currency='€', country='Spain', email='john.doe@example.com', type='Savings')
    
    assert account.balance == 0.0
    assert account.status == "Active"
    assert account.created_at is not None  # Ensure created_at is set
    print(account.created_at)

def test_account_creation_missing_required_fields():
    with pytest.raises(ValueError, match="Name cannot be empty."):
        Account(name='', currency='€', country='Spain', email='john.doe@example.com', type='Savings')

    with pytest.raises(TypeError):
        account = Account(name='John Doe', currency='€', email='john.doe@example.com', type='Savings')

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database
    with app.app_context():
        db.create_all()  # Create all tables
        yield app.test_client()  # Provide the test client

def test_duplicate_account_number(test_client):
    """
    GIVEN an Account model
    WHEN two Accounts are created with the same account number
    THEN check that a IntegrityError is raised
    """
    # Create the first account
    account1 = Account(name='John Doe', currency='€', country='Spain', email='john@example.com', type='Savings')
    db.session.add(account1)
    db.session.commit()

    # Create the second account with the same account number
    account2 = Account(name='Jane Doe', currency='€', country='Spain', email='jane@example.com', type='Savings')
    account2.account_number = account1.account_number  # Set the same account number

    with pytest.raises(Exception):  # Adjust this to IntegrityError if specific
        db.session.add(account2)
        db.session.commit()  # This should raise an error
