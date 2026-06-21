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
    
    # The crucial admin flag
    is_admin = Column(Boolean, default=False)
    
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with hashing"""
        if name == "password":
            value = generate_password_hash(value)
        super().__setattr__(name, value)

    def check_password(self, value):
        """Verifies if a given password matches the stored hashed password."""
        return check_password_hash(self.password, value)

    def to_dict(self):
        """Forces the is_admin flag to be sent to React, and hides the password"""
        user_dict = super().to_dict()
        user_dict['is_admin'] = getattr(self, 'is_admin', False)
        if 'password' in user_dict:
            del user_dict['password'] # Never send password hashes to frontend!
        return user_dict
