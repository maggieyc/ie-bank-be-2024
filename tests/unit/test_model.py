from iebank_api.models import Account
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

    with pytest.raises(TypeError):
        account = Account(name='John Doe', currency='€', email='john.doe@example.com', type='Savings')