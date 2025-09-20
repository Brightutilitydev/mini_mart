#!/usr/bin/env python3
"""
Repository class for managing User operations
Provides methods to create, retrieve, update, and delete User objects.
"""

from models import storage
from models.user import User


class UserRepo:
    """Repository class to manage user operations"""
    @classmethod
    def new(cls, **kwargs) -> User:
        """
        Create and store a new user.
        
        Required fields:
            - first_name (str)
            - last_name (str)
            - username (str, unique)
            - email (str, unique)
            - password (str)

        Optional fields:
            - other_name (str)
            - address (str)

        Returns:
            User: the created user instance.

        Raises:
            ValueError: if required fields are missing.
        """
        required_fields = ["first_name", "last_name", "username", "email", "password"]
        for field in required_fields:
            if not kwargs.get(field):
                raise ValueError(f"Missing required field: {field}")

        user = User(
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"],
            other_name=kwargs.get("other_name"),
            username=kwargs["username"],
            email=kwargs["email"],
            address=kwargs.get("address"),
            password=kwargs["password"],
        )
        user.save()
        return user

    @classmethod
    def get(cls, user_id: str) -> User | None:
        """
        Retrieve a user by ID.

        Args:
            user_id (str): UUID of the user.

        Returns:
            User | None: The user instance if found, else None.
        """
        return storage.get(User, user_id)

    @classmethod
    def all(cls) -> list[User]:
        """
        Retrieve all users.

        Returns:
            list[User]: List of all user instances.
        """
        return storage.all(User)

    @classmethod
    def update(cls, **kwargs) -> User | None:
        """
        Update user details.

        Args:
            kwargs: must include "id" of the user and the fields to update.

        Returns:
            User | None: Updated user instance, or None if not found/invalid.
        """
        user_id = kwargs.get("id")
        if not user_id:
            return None

        user = cls.get(user_id)
        if not user:
            return None

        for key, value in kwargs.items():
            if key != "id" and hasattr(user, key):
                setattr(user, key, value)
        user.save()
        return user

    @classmethod
    def delete(cls, user_id: str) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id (str): UUID of the user.

        Returns:
            bool: True if deleted, False otherwise.
        """
        user = cls.get(user_id)
        if not user:
            return False
        storage.delete(user)
        storage.save()
        return True

    @classmethod
    def get_by_username(cls, username: str) -> User | None:
        """
        Retrieve a user by username.

        Args:
            username (str): The username to search.

        Returns:
            User | None: User if found, else None.
        """
        return storage.get_by_attr(User, username=username)

    @classmethod
    def get_by_email(cls, email: str) -> User | None:
        """
        Retrieve a user by email.

        Args:
            email (str): The email to search.

        Returns:
            User | None: User if found, else None.
        """
        return storage.get_by_attr(User, email=email)
