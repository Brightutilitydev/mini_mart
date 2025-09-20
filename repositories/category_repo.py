#!/usr/bin/env python3
"""Management of category items"""

from models import storage
from models.category import Category


class CategoryRepo:
    """Repository class to manage category operations"""

    @classmethod
    def new(cls, **kwargs) -> Category:
        """
        Create and store a new category.
        Args:
            name (str): Category name (required)
            parent_id (str): Optional parent category UUID
        Returns:
            Category: The newly created category
        Raises:
            ValueError: If required fields are missing
        """
        if not kwargs.get("name"):
            raise ValueError("Category name is not set")

        category = Category(
            name=kwargs["name"],
            parent_id=kwargs.get("parent_id"),
        )
        category.save()
        return category

    @classmethod
    def get(cls, category_id: str) -> Category | None:
        """Retrieve a category by ID"""
        return storage.get(Category, category_id)

    @classmethod
    def all(cls) -> list[Category]:
        """Retrieve all categories"""
        return storage.all(Category)

    @classmethod
    def update(cls, **kwargs) -> Category | None:
        """
        Update category details.
        Args:
            id (str): Category ID (required)
            name (str): Optional new name
            description (str): Optional new description
            parent_id (str): Optional new parent category ID
        Returns:
            Category | None: Updated category if found, else None
        """
        if not kwargs:
            return None
        category_id = kwargs.get("id")
        if not category_id:
            return None

        category = cls.get(category_id)
        if not category:
            return None

        for key, value in kwargs.items():
            if hasattr(category, key) and key != "id":
                setattr(category, key, value)

        category.save()
        return category

    @classmethod
    def delete(cls, category_id: str) -> bool:
        """Delete a category by ID"""
        category = cls.get(category_id)
        if not category:
            return False
        storage.delete(category)
        storage.save()
        return True


    @classmethod
    def get_by_name(cls, name: str) -> Category | None:
        """Find a category by exact name"""
        return storage.get_by_attr(Category, name=name)

    @classmethod
    def get_subcategories(cls, parent_id: str) -> list[Category]:
        """Retrieve all subcategories of a given parent category"""
        return storage.get_by_attr(Category, parent_id=parent_id)
