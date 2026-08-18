#!/usr/bin/env python3
"""User Model"""

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from models.base_model import Base, BaseModel

class User(BaseModel, Base):
    """Represents a user in the Mini Mart system."""
    __tablename__ = "users"

    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False, index=True)
    phone_number = Column(String(32), unique=True, nullable=True, index=True)
    whatsapp_number = Column(String(32), unique=True, nullable=False, index=True)
    address = Column(String(256), nullable=True)
    password = Column(String(256), nullable=False)

    # Access flags
    is_admin = Column(Boolean, default=False)
    is_super_admin = Column(Boolean, default=False)

    # Payment details supported by the app
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes a user while preserving legacy fields and new flags."""
        super().__init__(*args, **kwargs)
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.email = kwargs.get("email", "")
        self.phone_number = kwargs.get("phone_number", "")
        self.whatsapp_number = kwargs.get("whatsapp_number", "")
        self.address = kwargs.get("address", "")
        self.is_admin = kwargs.get("is_admin", False)
        self.is_super_admin = kwargs.get("is_super_admin", False)

        self.bank_name = kwargs.get("bank_name", "")
        self.account_number = kwargs.get("account_number", "")
        self.account_name = kwargs.get("account_name", "")

    def __setattr__(self, name, value):
        """Hashes the password before storing it while keeping other attributes intact."""
        if name == "password" and value is not None:
            value = generate_password_hash(value)
        super().__setattr__(name, value)

    def check_password(self, value):
        """Verifies if a given password matches the stored hashed password."""
        return check_password_hash(self.password, value)

    def to_dict(self):
        """Includes access flags and payment details while hiding the password."""
        user_dict = super().to_dict()
        user_dict['is_admin'] = getattr(self, 'is_admin', False)
        user_dict['is_super_admin'] = getattr(self, 'is_super_admin', False)

        user_dict['bank_name'] = getattr(self, 'bank_name', '')
        user_dict['account_number'] = getattr(self, 'account_number', '')
        user_dict['account_name'] = getattr(self, 'account_name', '')

        if 'password' in user_dict:
            del user_dict['password']
        return user_dict