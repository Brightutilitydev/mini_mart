#!/usr/bin/env python3
"""User Model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class User(Base, BaseModel):
    """Define a user and their properties"""

    __tablename__ = "users"

    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    other_name = Column(String(128), nullable=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    address = Column(String(256), nullable=True)
    password = Column(String(256), nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
