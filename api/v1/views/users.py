#!/usr/bin/env python3
"""Manage users"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User
from repositories.user_repo import UserRepo

@app_views.route('/users', methods=['GET'])
def get_all_users():
    user_list = UserRepo.all()
    user_list = [entry.to_dict() for entry in user_list]
    return jsonify(user_list)

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserRepo.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "user not found"}), 404

@app_views.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new = UserRepo.new(**data)
    except ValueError as e:
        return jsonify({
            "error": "incorrect/incomplete parameters",
            "message": str(e)
        }), 400
    return jsonify(new.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    # ✅ BUG FIX: Pass the ID explicitly as a named argument to the repository
    res = UserRepo.update(id=user_id, **data)
    
    if not res:
        return jsonify({"error": "user not found"}), 404
    return jsonify(res.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    deleted = UserRepo.delete(user_id)
    if deleted:
        return jsonify({"success": "OK"}), 200
    return jsonify({"error": "user not found"}), 404


@app_views.route('/store-settings', methods=['GET'])
def get_store_settings():
    """Public endpoint for the cart to fetch the Admin's bank details"""
    admin = storage.get_by_attr(User, is_admin=True)
    if not admin:
        admin = storage.get_by_attr(User, is_admin=1)

    if admin:
        return jsonify({
            "bank_name": getattr(admin, "bank_name", ""),
            "account_number": getattr(admin, "account_number", ""),
            "account_name": getattr(admin, "account_name", "")
        }), 200

    return jsonify({"error": "Store settings not found"}), 404
