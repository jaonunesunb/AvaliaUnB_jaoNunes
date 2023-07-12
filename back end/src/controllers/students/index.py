from flask import Blueprint, request, jsonify, make_response, Response
from src.middlewares.index import authenticate_token, check_admin
from src.services.students.index import create_user, edit_user, get_user_by_email, get_users, get_user_by_id, delete_user, convert_image_to_base64, login

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users/register', methods=['POST'])
def create_user_controller():
    data = request.get_json()
    
    image_path = data["foto"]
    foto_binario = convert_image_to_base64(image_path)
    user = create_user(data["nome"], data["email"], data["senha"], data["matricula"], data["curso"], foto_binario, data["is_adm"])
    
    return jsonify(user), 201

@users_blueprint.route('/users/<int:user_id>', methods=['PATCH'])
@authenticate_token
def edit_user_controller(user_id):
    data = request.json
    image_path = data["foto"]
    
    foto_binario = convert_image_to_base64(image_path)
    
    user = edit_user(user_id, data['nome'], data['email'], data['senha'], data['curso'], foto_binario)
    return jsonify(user)

@users_blueprint.route('/users', methods=['GET'])
@authenticate_token
def get_users_controller():
    users = get_users()
    return jsonify(users)

@users_blueprint.route('/users/<int:user_id>', methods=['GET'])
@authenticate_token
def get_user_by_id_controller(user_id):
    user = get_user_by_id(user_id)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
@users_blueprint.route('/users/<string:email>', methods=['GET'])
@authenticate_token
def get_user_by_email_controller(email):
    user = get_user_by_email(email)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

@users_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@authenticate_token
def delete_user_controller(user_id):
    delete_user(user_id)
    return jsonify({'message': 'Usuário excluído com sucesso'})

@users_blueprint.route('/users/login', methods=['POST'])
def login_controller():
    data = request.get_json()
    email = data['email']
    senha = data['senha']

    return login(email, senha)

