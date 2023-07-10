from flask import Blueprint, request, jsonify
from src.services.students.index import create_user, edit_user, get_users, get_user_by_id, delete_user, convert_image_to_base64, login

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods=['POST'])
def create_user_controller():
    data = request.get_json()
    
    image_path = data["foto"]

    # Converte a imagem para base64
    foto_binario = convert_image_to_base64(image_path)

    # Chama a função create_user() com os dados atualizados
    create_user(data["nome"], data["email"], data["senha"], data["matricula"], data["curso"], foto_binario, data["is_adm"])
    
    return jsonify({"message": "Usuário criado com sucesso"}), 201

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

@users_blueprint.route('/users/login', methods=['POST'])
def login_controller():
    data = request.get_json()
    email = data['email']
    senha = data['senha']

    token = login(email, senha)

    if token:
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Falha na autenticação'}), 401