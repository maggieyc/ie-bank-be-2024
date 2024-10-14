from iebank_api import db
from datetime import datetime
import string, random
from sqlalchemy.orm import validates
import re

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default = 0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    country = db.Column(db.String(32), nullable = False)
    email = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.account_number
    
    @validates('type')
    def validate_type(self, key, value):
        # Check if the email is empty
        if not value or value.strip() == "":
            raise ValueError("Type cannot be empty.")
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, value):
            raise ValueError(f"Invalid email address: {value}.")

        return value

    @validates('country')
    def validate_country(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Country cannot be empty.")
        return value
    
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Name cannot be empty.")
        return value
    

    @validates('currency')
    def validate_currency(self, key, value):
        allowed_currencies = ['$', '€']
        if value not in allowed_currencies:
            raise ValueError(f"Invalid currency: {value}. Must be one of {allowed_currencies}.")
        return value

    def __init__(self, name, currency, country, email, type):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.balance = 0.0
        self.status = "Active"
        self.currency = currency
        self.country = country
        self.email = email
        self.type = type
        self.created_at = datetime.now()