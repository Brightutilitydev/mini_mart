#!/usr/bin/env python3
"""Manage products"""

import os
from flask import (
    jsonify, request, current_app
)
from api.v1.views import app_views
from api.v1.views.auth import admin_required
from flask_jwt_extended import jwt_required
from repositories.product_repo import ProductRepo

from dotenv import load_dotenv
load_dotenv()

import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key = os.getenv('CLOUDINARY_API_KEY'),
  api_secret = os.getenv('CLOUDINARY_API_SECRET'),
  secure = True
)

allowed_extensions = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".webp", ".heic", ".heif", ".svg", ".ico", ".jfif", ".avif"
}

def save_image(image):
    """Upload an image directly to Cloudinary and return the secure URL"""
    ext = os.path.splitext(image.filename)[-1].lower()
    if ext not in allowed_extensions:
        return None

    try:
        upload_result = cloudinary.uploader.upload(image)
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload failed: {e}")
        return None

@app_views.route('/products', methods=['GET'])
def get_all_products():
    """Get all products"""
    prod_list = ProductRepo.all()
    prod_list = [entry.to_dict() for entry in prod_list]
    return jsonify(prod_list)

@app_views.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    product = ProductRepo.get(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "product not found"}), 404

@app_views.route('/products', methods=['POST'])
@jwt_required()
@admin_required()
def create_product():
    """Create a new product"""
    image_url = None
    images = request.files.getlist("images")

    if images:
        image = images[0]
        image_url = save_image(image)
        if not image_url:
            return jsonify({"error": "invalid image type or upload failed"}), 400

    data = request.form.to_dict()
    if image_url:
        data["image_url"] = image_url

    try:
        new = ProductRepo.new(**data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(new.to_dict()), 201

@app_views.route('/products/<product_id>', methods=['PUT'])
@jwt_required()
@admin_required()
def update_product(product_id):
    """Update an existing product"""
    product = ProductRepo.get(product_id)
    if not product:
        return jsonify({"error": "product not found"}), 404

    image_url = None
    images = request.files.getlist("images")

    if images:
        image = images[0]
        new_url = save_image(image)
        if not new_url:
            return jsonify({"error": "invalid image type or upload failed"}), 400
        
        if getattr(product, "image_url", None) and 'res.cloudinary.com' in product.image_url:
            try:
                public_id = product.image_url.split('/')[-1].split('.')[0]
                cloudinary.uploader.destroy(public_id)
            except Exception as e:
                print(f"Could not remove old image from Cloudinary: {e}")
                
        image_url = new_url

    data = request.form.to_dict() if not request.is_json else request.get_json()
    if image_url:
        data["image_url"] = image_url

    res = ProductRepo.update(product_id, **data)
    return jsonify(res.to_dict()), 200

@app_views.route('/products/category/<category_id>', methods=['GET'])
def get_products_by_category(category_id):
    """Get products by category"""
    products = ProductRepo.get_products_by_category(category_id)
    if not products:
        return jsonify({"error": "category not found"}), 404
    return jsonify([product.to_dict() for product in products]), 200

@app_views.route('/products/<product_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def remove_product(product_id):
    """Delete a product"""
    product = ProductRepo.get(product_id)
    if not product:
        return jsonify({"error": "product not found"}), 404

    # Delete the image from Cloudinary
    if getattr(product, "image_url", None) and 'res.cloudinary.com' in product.image_url:
        try:
            public_id = product.image_url.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print(f"Could not remove image from Cloudinary: {e}")

    deleted = ProductRepo.delete(product_id)
    if deleted:
        return jsonify({"success": "OK"}), 200

    return jsonify({"error": "product not found"}), 404