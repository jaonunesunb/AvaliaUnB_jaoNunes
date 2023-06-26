from flask import Blueprint, request, jsonify
from services.students.index import create_user, edit_user, get_users, get_user_by_id, delete_user

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods=['POST'])
def create_user_controller():
    data = request.json
    create_user(data['nome'], data['email'], data['senha'], data['matricula'], data['curso'])
    return jsonify('User created successfully'), 201

@users_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def edit_user_controller(user_id):
    data = request.json
    edit_user(user_id, data['nome'], data['email'], data['senha'], data['curso'])
    return jsonify('User updated successfully')

@users_blueprint.route('/users', methods=['GET'])
def get_users_controller():
    users = get_users()
    return jsonify(users)

@users_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id_controller(user_id):
    user = get_user_by_id(user_id)
    return jsonify(user)

@users_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_controller(user_id):
    delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'})
