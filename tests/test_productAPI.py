#!/usr/bin/env python3
"""Test Product API"""

import requests

BASE_URL = "http://localhost:5000/products"

# Sample product data
sample_product = {
    "name": "Test Product",
    "price": 1999,
    "volume": 5000,
    "description": "This is a test product"
}

def create_product(product_data):
    """Create a product"""
    response = requests.post(f"{BASE_URL}/create", json=product_data)
    print("CREATE:", response.json())
    return response

def get_products():
    """Get all products"""
    response = requests.get(BASE_URL)
    print("READ (all products):", response.json())
    return response.json()

def update_product(product_id, updated_data):
    """Update a product"""
    updated_data['id'] = product_id
    response = requests.put(f"{BASE_URL}/update", json=updated_data)
    print("UPDATE:", response.json())
    return response

def delete_product(product_id):
    """Delete a product"""
    response = requests.delete(f"{BASE_URL}/{product_id}")
    print("DELETE:", response.json())
    return response

if __name__ == "__main__":
    # 1. Create product
    create_product(sample_product)

    # 2. Get all products and grab the last one (newly created)
    products = get_products()
    new_product_id = ""
    if products:
        for product in products:
            if product['name'] == sample_product['name'] and product['volume'] == sample_product['volume']:
                new_product_id = product['id']
        print("New product ID:", new_product_id)

        # 3. Update product
        updated_data = {
            "name": "Updated Product",
            "price": 29.99,
            "volume": 10,
            "description": "This product was updated"
        }
        update_product(new_product_id, updated_data)

        # 4. Delete product
        delete_product(new_product_id)
