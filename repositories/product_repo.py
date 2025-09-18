#!/usr/bin/env python3
"""Management of product items"""

from models import storage
from models.product import Product
from models.category import Category


class ProductRepo:
    """Repository class to manage product operations"""
    @classmethod
    def new_product(cls, **kwargs) -> Product:
        """Create and store a new product"""
        if not kwargs.get("name"):
            raise ValueError("Product name is not set")
        if not kwargs.get("price"):
            raise ValueError("Product price is not set")
        if not kwargs.get("volume"):
            raise ValueError("Prduct volume is not set")
        if not kwargs.get("category_id"):
            kwargs['category_id'] = None
        product = Product(
                name=kwargs['name'],
                volume=kwargs['volume'],
                category_id=kwargs['category_id'],
#               price=kwargs['price'],
                brand=None,
                description=None
            )
        product.save()
        return product

    def get_product_by_id(self, product_id: str) -> Product | None:
        """Retrieve a product by ID"""
        return storage.get(Product, product_id)

    def get_all_products(self) -> list[Product]:
        """Retrieve all products"""
        return storage.all(Product).values()

    def update_product(self, product_id: str, **kwargs) -> Product | None:
        """Update product details"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        product.save()
        return product

    def delete_product(self, product_id: str) -> bool:
        """Delete a product"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        storage.delete(product)
        storage.save()
        return True

    def get_product_by_name(self, name: str) -> Product | None:
        """Find a product by exact name"""
        return storage.session.query(Product).filter_by(name=name).first()

    def get_products_by_category(self, category_id: str) -> list[Product]:
        """Retrieve all products in a given category"""
        return storage.session.query(Product).filter_by(category_id=category_id).all()

    def count_products_in_category(self, category_id: str) -> int:
        """Count how many products belong to a category"""
        return storage.session.query(Product).filter_by(category_id=category_id).count()

    def move_product_to_category(self, product_id: str, new_category_id: str) -> Product | None:
        """Change product's category"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        product.category_id = new_category_id
        storage.save()
        return product
