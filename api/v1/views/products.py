#!/usr/bin/env python3
"""Manage products"""

import os
import uuid
from flask import (
    jsonify, request, url_for, current_app, send_from_directory
)
from werkzeug.utils import secure_filename
from api.v1.views import app_views
from repositories.product_repo import ProductRepo

allowed_extensions = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".webp", ".heic", ".heif", ".svg", ".ico", ".jfif", ".avif"
}

def save_image(image):
    """Save an uploaded image with a unique filename, return its URL"""
    ext = os.path.splitext(image.filename)[-1].lower()
    if ext not in allowed_extensions:
        return None

    unique_name = f"{uuid.uuid4().hex}{ext}"
    filename = secure_filename(unique_name)

    saved_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    image.save(saved_path)

    return url_for("app_views.get_image", filename=filename, _external=True)

@app_views.route('/products', methods=['GET'])
# @admin_required()
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

@app_views.route("/images/<filename>")
def get_image(filename):
    """Get product image"""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@app_views.route('/products', methods=['POST'])
# @admin_required()  <--- DISABLED FOR CLIENT DEMO
def create_product():
    """Create a new product"""
    image_url = None
    images = request.files.getlist("images")

    if images:
        image = images[0]
        image_url = save_image(image)
        if not image_url:
            return jsonify({"error": "invalid image type"}), 400

    data = request.form.to_dict()
    if image_url:
        data["image_url"] = image_url

    try:
        new = ProductRepo.new(**data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(new.to_dict()), 201

@app_views.route('/products/<product_id>', methods=['PUT'])
# @admin_required() <--- DISABLED FOR CLIENT DEMO
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
            return jsonify({"error": "invalid image type"}), 400
        if getattr(product, "image_url", None):
            try:
                old_filename = os.path.basename(product.image_url)
                old_path = os.path.join(current_app.config["UPLOAD_FOLDER"], old_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            except Exception as e:
                current_app.logger.warning(f"Could not remove old image: {e}")
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
# @admin_required() <--- DISABLED FOR CLIENT DEMO
def remove_product(product_id):
    """Delete a product"""
    product = ProductRepo.get(product_id)
    if not product:
        return jsonify({"error": "product not found"}), 404

    if getattr(product, "image_url", None):
        try:
            filename = os.path.basename(product.image_url)
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            current_app.logger.warning(f"Could not remove image: {e}")

    deleted = ProductRepo.delete(product_id)
    if deleted:
        return jsonify({"success": "OK"}), 200

    return jsonify({"error": "product not found"}), 404