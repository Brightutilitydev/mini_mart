#!/usr/bin/env python3
"""Manage products"""

from api.v1.views import app_views
from models import storage
from models.product import Product
from flask import jsonify, request
from repositories.product_repo import ProductRepo


@app_views.route('/', methods=['GET'])
def get_all_products():
    """Return the a json of all products in db"""
    prod_list = storage.all(Product)
    prod_list = [entry.to_dict() for entry in prod_list]
    return jsonify(prod_list)


@app_views.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Return a product based on id"""
    product = storage.get(Product, product_id)
    print(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "product not found"}), 404



@app_views.route('/create', methods=['POST', 'PUT'])
def create_product():
    """Create a new product"""
    data = request.get_json()
    try:
        new = ProductRepo.new_product(**data)
    except ValueError as e:
        return jsonify({"error": "incorrect/incomplete parameters", "message": str(e)}), 400
    return jsonify({"success": "product created"}), 201
