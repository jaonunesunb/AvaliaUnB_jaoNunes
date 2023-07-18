import os
from flask import Blueprint, request, jsonify, make_response, render_template, session, flash, redirect
from src.services.reports.index import get_denuncias_by_estudante_id
from src.controllers.reports.index import get_all_reports
from src.db_connection.connection import get_db_connection
from src.services.avaluations.index import get_avaliacoes_by_userID
from src.middlewares.index import check_admin, is_authenticated
from src.services.students.index import create_user, edit_user, get_user_by_email, get_users, get_user_by_id, delete_user, convert_image_to_base64

users_blueprint = Blueprint('users', __name__)

from flask import request
from werkzeug.utils import secure_filename

import os
from flask import Blueprint, jsonify, request, redirect
from werkzeug.utils import secure_filename

users_blueprint = Blueprint('users_blueprint', __name__)

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

    if user:
        return redirect("/")
    else:
        return jsonify(user), 201


@users_blueprint.route('/users/<int:user_id>', methods=['PUT'])
@is_authenticated
def edit_user_controller(user_id):
    data = request.form

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    curso = data.get('curso')
    foto = request.files.get('foto')

    user = get_user_by_id(user_id)

    if nome is None:
        nome = user['nome']
    if email is None:
        email = user['email']
    if senha is None:
        senha = user['senha']
    if curso is None:
        curso = user['curso']

    foto_data = None

    if foto:
        foto_data = foto.read()

    user = edit_user(user_id, nome, email, senha, curso, foto_data, user['is_adm'])

    if user is None:
        return jsonify({'message': 'Nenhum campo fornecido para atualização.'}), 400

    return jsonify(user)

@users_blueprint.route('/users', methods=['GET'])
def get_users_controller():
    users = get_users()
    return jsonify(users)

@users_blueprint.route('/users/<int:user_id>')
@is_authenticated
def user_profile(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    avaliacoes = get_avaliacoes_by_userID(user_id)

    if user['is_adm']:
        denuncias = get_all_reports()
    else:
        denuncias = get_denuncias_by_estudante_id(user_id)

    return render_template('userPage.html', user=user,
        avaliacoes=avaliacoes,
        denuncias=denuncias)


@users_blueprint.route('/users/<int:user_id>', methods=['GET'])
@is_authenticated
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
@is_authenticated
def delete_user_controller(user_id):
    delete_user(user_id)
    return jsonify({'message': 'Usuário excluído com sucesso'})

@users_blueprint.route('/users/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT id, nome, senha, is_adm FROM Estudantes WHERE email = %s
    '''
    cursor.execute(select_query, (email,))
    user = cursor.fetchone()

    if user:
        user_id, nome, stored_password, is_adm = user
        if senha == stored_password:
            session['user_id'] = user_id
            session['is_adm'] = is_adm
            session['nome'] = nome
            flash('Conectou-se com sucesso!', category='success')
            return redirect('/')
        else:
            return jsonify({'message': 'E-mail ou Senha incorretos'}), 401
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 401

@users_blueprint.route('/logout')
@is_authenticated
def logout():
    session.clear()
    flash('LogOut bem sucedido.', category='success')
    return redirect('/')