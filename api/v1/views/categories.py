#!/usr/bin/env python3
"""
Category API routes

This module manages CRUD operations for categories.
It provides endpoints to create, read, update, and delete categories.

Routes:
    GET    /categories           -> Get all categories
    POST   /categories/create    -> Create a new category
    GET    /categories/<id>      -> Get a specific category by ID
    PUT    /categories           -> Update an existing category
    DELETE /categories/<id>      -> Delete a category
"""


from api.v1.views import app_views
from flask import jsonify, request
from repositories.category_repo import CategoryRepo


@app_views.route('/categories', methods=['GET'])
def get_all_categories():
    """
    Return a JSON list of all categories in the database.
    Returns:
        200: List of categories
    """
    cat_list = CategoryRepo.all()
    cat_list = [entry.to_dict() for entry in cat_list]
    return jsonify(cat_list)


@app_views.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    """
    Return a category by ID.
    Args:
        category_id (str): Category UUID
    Returns:
        200: Category object
        404: If not found
    """
    category = CategoryRepo.get(category_id)
    if category:
        return jsonify(category.to_dict())
    return jsonify({"error": "category not found"}), 404


@app_views.route('/categories/create', methods=['POST', 'PUT'])
def create_category():
    """
    Create a new category.
    Request JSON:
        {
            "name": "string",          # required
            "description": "string",   # optional
            "parent_id": "uuid"        # optional
        }
    Returns:
        201: {"success": "OK"}
        400: {"error": "..."}
    """
    data = request.get_json()
    try:
        new = CategoryRepo.new(**data)
    except ValueError as e:
        return jsonify({
            "error": "incorrect/incomplete parameters",
            "message": str(e)
        }), 400
    return jsonify({"success": "OK"}), 201


@app_views.route('/categories/<category_id>', methods=['DELETE'])
def remove_category(category_id):
    """
    Delete a category by ID.
    Args:
        category_id (str): Category UUID
    Returns:
        201: {"success": "OK"} if deleted
        404: {"error": "category not found"} if not found
    """
    data = CategoryRepo.delete(category_id)
    if data:
        return jsonify({"success": "OK"}), 201
    return jsonify({"error": "category not found"}), 404


@app_views.route('/categories/update', methods=['PUT'])
def update_category():
    """
    Update a category.
    Request JSON:
        {
            "id": "uuid",              # required
            "name": "string",          # optional
            "description": "string",   # optional
            "parent_id": "uuid"        # optional
        }
    Returns:
        200: {"success": "OK"} if updated
        404: {"error": "category not found"} if not found
    """
    data = request.get_json()
    res = CategoryRepo.update(**data)
    if not res:
        return jsonify({"error": "category not found"}), 404
    return jsonify({"success": "OK"}), 200
