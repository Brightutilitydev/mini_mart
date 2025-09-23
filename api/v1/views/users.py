#!/usr/bin/env python3
"""Manage users"""

from api.v1.views import app_views
from flask import jsonify, request
from repositories.user_repo import UserRepo


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    """
    user_list = UserRepo.all()
    user_list = [entry.to_dict() for entry in user_list]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The user UUID
    responses:
      200:
        description: User found
        schema:
          $ref: '#/definitions/User'
      404:
        description: User not found
    """
    user = UserRepo.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "user not found"}), 404


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/User'
    responses:
      201:
        description: User created successfully
        schema:
          $ref: '#/definitions/User'
      400:
        description: Invalid input
    """
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
    """
    Update a user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The user UUID
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/User'
    responses:
      200:
        description: User updated successfully
        schema:
          $ref: '#/definitions/User'
      404:
        description: User not found
    """
    data = request.get_json()
    res = UserRepo.update(user_id, **data)
    if not res:
        return jsonify({"error": "user not found"}), 404
    return jsonify(res.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    """
    Delete a user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The user UUID
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    deleted = UserRepo.delete(user_id)
    if deleted:
        return jsonify({"success": "OK"}), 200
    return jsonify({"error": "user not found"}), 404
