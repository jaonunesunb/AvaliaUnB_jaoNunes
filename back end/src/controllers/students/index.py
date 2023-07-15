import os
from flask import Blueprint, request, jsonify, make_response
from src.middlewares.index import authenticate_token, check_admin
from src.services.students.index import create_user, edit_user, get_user_by_email, get_users, get_user_by_id, delete_user, convert_image_to_base64, login

users_blueprint = Blueprint('users', __name__)

from flask import request
from werkzeug.utils import secure_filename

@users_blueprint.route('/users/register', methods=['POST'])
def create_user_controller():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    matricula = request.form.get('matricula')
    curso = request.form.get('curso')
    foto = request.files.get('foto')

    if foto is not None and foto.filename != '':
        filename = secure_filename(foto.filename)
        foto.save(filename)
        foto_base64 = convert_image_to_base64(filename)
        os.remove(filename)
    else:
        foto_base64 = None

    user = create_user(nome, email, senha, matricula, curso, foto_base64, is_adm=False)

    return jsonify(user), 201


@users_blueprint.route('/users/<int:user_id>', methods=['PATCH'])
def edit_user_controller(user_id):
    data = request.get_json()

    image_path = data["foto"]
    foto_binario = convert_image_to_base64(image_path)

    user = edit_user(user_id, data['nome'], data['email'], data['senha'], data['curso'], foto_binario)
    return jsonify(user)

@users_blueprint.route('/users', methods=['GET'])
def get_users_controller():
    users = get_users()
    return jsonify(users)

@users_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id_controller(user_id):
    user = get_user_by_id(user_id)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

@users_blueprint.route('/users/<string:email>', methods=['GET'])
def get_user_by_email_controller(email):
    user = get_user_by_email(email)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

@users_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_controller(user_id):
    delete_user(user_id)
    return jsonify({'message': 'Usuário excluído com sucesso'})

@users_blueprint.route('/users/login', methods=['POST'])
def login_controller():
    email = request.form.get('email')
    senha = request.form.get('senha')

    response = login(email, senha)
    return make_response(response)

