#!/usr/bin/env python3
"""Manage user properties"""

from models import storage
from models.user import User


class UserRepository:
    """User properties"""

    def get_by_id(self, user_id: int):
        return storage.get(User, user_id)

    def get_by_email(self, email: str):
        users = storage.all(User)
        for user in users:
            if user.email == email:
                return user

    def get_by_username(self, username: str):
        users = storage.all(User)
        for user in users:
            if user.username == username:
                return user

    def list_all(self) -> list[User]:
        return storage.all(User)

