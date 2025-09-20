#!/usr/bin/env python3
"""Manage users"""

from api.v1.views import app_views
from flask import jsonify, request
from repositories.user_repo import UserRepo


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """Return the a json of all users in db"""
    user_list = UserRepo.all()
    user_list = [entry.to_dict() for entry in user_list]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Return a user based on id"""
    user = UserRepo.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "user not found"}), 404


@app_views.route('/users/create', methods=['POST', 'PUT'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    try:
        new = UserRepo.new(**data)
    except ValueError as e:
        return jsonify({"error": "incorrect/incomplete parameters", "message": str(e)}), 400
    return jsonify({"success": "OK"}), 201


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    """Delete a user"""
    data = UserRepo.delete(user_id)
    if data:
        return jsonify({"success": "OK"}), 201
    return jsonify({"error": "user not found"})


@app_views.route('/users/update', methods=['PUT'])
def update_user():
    """Update user"""
    data = request.get_json()
    res = UserRepo.update(**data)
    if not res:
        return jsonify({"error": "user not found"})
    return jsonify({"success": "OK"} )
