from flask import g, make_response, jsonify
import os
import re
from src.db_connection.connection import get_db_connection
from flask_login import current_user 
import jwt
import base64
import datetime
from dotenv import dotenv_values

env_variables = dotenv_values()

def create_user(nome, email, senha, matricula, curso, foto, is_adm=False):
    if not re.match(r'^\d{9}@aluno.unb.br$', email):
        return None

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Estudantes (nome, email, senha, matricula, curso, foto, is_adm)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, nome, email, matricula, curso, is_adm
    '''
    cursor.execute(insert_query, (nome, email, senha, matricula, curso, foto, is_adm))
    conn.commit()

    user = cursor.fetchone() 
    user_dict = {
        'id': user[0],
        'nome': user[1],
        'email': user[2],
        'matricula': user[3],
        'curso': user[4],
        'is_adm': user[5],
        'foto': base64.b64encode(foto.encode('utf-8')).decode('utf-8') if foto else None
    }

    cursor.close()
    conn.close()

    return user_dict


def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Estudantes WHERE email = %s
    '''
    cursor.execute(select_query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        user_dict = {
            'id': user[0],
            'nome': user[1],
            'email': user[2],
            'matricula': user[3],
            'curso': user[4],
            'is_adm': user[5],
            'foto': base64.b64encode(user[6].encode('utf-8')).decode('utf-8') if user[6] else None
        }
        return user_dict
    else:
        return None

    
def edit_user(user_id, nome=None, email=None, senha=None, curso=None, foto=None, is_adm=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_values = []

    if nome is not None:
        update_values.append(('nome', nome))
    if email is not None:
        update_values.append(('email', email))
    if senha is not None:
        update_values.append(('senha', senha))
    if curso is not None:
        update_values.append(('curso', curso))
    if foto is not None:
        update_values.append(('foto', foto))
    if is_adm is not None:
        update_values.append(('is_adm', is_adm))

    set_clause = ', '.join([f'{field} = %s' for field, _ in update_values])

    update_query = f'''
        UPDATE Estudantes
        SET {set_clause}
        WHERE id = %s
        RETURNING id, nome, email, matricula, curso, foto, is_adm
    '''

    update_values.append(('user_id', user_id))
    update_values = [value for _, value in update_values]

    cursor.execute(update_query, update_values)
    conn.commit()

    user = cursor.fetchone()
    user_dict = {
        'id': user[0],
        'nome': user[1],
        'email': user[2],
        'matricula': user[3],
        'curso': user[4],
        'is_adm': user[6],
        'foto': base64.b64encode(user[5]).decode('utf-8') if user[5] else None
    }

    cursor.close()
    conn.close()

    return user_dict


def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT id, nome, email, matricula, curso, is_adm, foto FROM Estudantes
    '''
    cursor.execute(select_query)
    users = cursor.fetchall()

    user_list = []
    for user in users:
        user_dict = {
            'id': user[0],
            'nome': user[1],
            'email': user[2],
            'matricula': user[3],
            'curso': user[4],
            'is_adm': user[5],
            'foto': base64.b64encode(user[6]).decode('utf-8') if user[6] else None
        }           
        user_list.append(user_dict)

    cursor.close()
    conn.close()

    return user_list


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Estudantes WHERE id = %s
    '''
    cursor.execute(select_query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        user_dict = {
            'id': user[0],
            'nome': user[1],
            'email': user[2],
            'matricula': user[4],
            'curso': user[6],
            'is_adm': user[5],
            'foto': base64.b64encode(user[6].encode('utf-8')).decode('utf-8') if user[6] else None
        }
        return user_dict
    else:
        return None


def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    delete_query = '''
        DELETE FROM Estudantes WHERE id = %s
    '''
    cursor.execute(delete_query, (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

def login(email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT id, senha, is_adm FROM Estudantes WHERE email = %s
    '''
    cursor.execute(select_query, (email,))
    user = cursor.fetchone()

    if user:
        user_id, stored_password, is_adm = user
        if senha == stored_password:
            token = generate_token(user_id)
            g.token = token  
            g.is_adm = is_adm
            response_data = {'message': 'Autenticação bem-sucedida', 'token': token}
            response = make_response(jsonify(response_data), 200)
            response.set_cookie('token', token, httponly=True)
            current_user.id = user_id
            current_user.is_adm = is_adm

            return response
        else:
            return jsonify({'message': 'E-mail ou Senha incorretos'}), 401
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 401

def generate_token(user_id):
    secret_key = os.getenv('SECRET_KEY') 
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Estudantes WHERE id = %s
    '''
    cursor.execute(select_query, (user_id,))
    user = cursor.fetchone()

    column_names = [desc[0] for desc in cursor.description]
    user_dict = dict(zip(column_names, user))
    is_admin = user_dict.get('is_admin')
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': expiration_time
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")
