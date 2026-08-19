#!/usr/bin/env python3
"""
Category API routes
This module manages CRUD operations for categories.
"""

from api.v1.views import app_views
from flask import jsonify, request
from api.v1.views.auth import admin_required
from flask_jwt_extended import jwt_required
from repositories.category_repo import CategoryRepo

@app_views.route('/categories', methods=['GET'])
def get_all_categories():
    """Get all categories"""
    cat_list = CategoryRepo.all()
    cat_list = [entry.to_dict() for entry in cat_list]
    return jsonify(cat_list)

@app_views.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    """Get category by ID"""
    category = CategoryRepo.get(category_id)
    if category:
        return jsonify(category.to_dict())
    return jsonify({"error": "category not found"}), 404

@app_views.route('/categories', methods=['POST'])
@jwt_required()
@admin_required()
def create_category():
    """Create a new category"""
    data = request.get_json()
    try:
        new = CategoryRepo.new(**data)
    except ValueError as e:
        return jsonify({
            "error": "incorrect/incomplete parameters",
            "message": str(e)
        }), 400
    return jsonify({"success": "OK"}), 201

@app_views.route('/categories/<category_id>', methods=['PUT'])
@jwt_required()
@admin_required()
def update_category(category_id):
    """Update an existing category"""
    data = request.get_json()
    res = CategoryRepo.update(id=category_id, **data)
    if not res:
        return jsonify({"error": "category not found"}), 404
    return jsonify({"success": "OK"}), 200

@app_views.route('/categories/<category_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def remove_category(category_id):
    """Delete a category"""
    data = CategoryRepo.delete(category_id)
    if data:
        return jsonify({"success": "OK"}), 200
    return jsonify({"error": "category not found"}), 404