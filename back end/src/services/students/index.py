from flask import jsonify, session, redirect, flash
import re
from src.db_connection.connection import get_cursor
import base64
from dotenv import dotenv_values
import bcrypt

env_variables = dotenv_values()

def create_user(nome, email, senha, matricula, curso, foto, is_adm=False):
    if not re.match(r'^\d{9}@aluno.unb.br$', email):
        return None
    
    hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    insert_query = '''
        INSERT INTO Estudantes (nome, email, senha, matricula, curso, foto, is_adm)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, nome, email, matricula, curso, is_adm
    '''
    with get_cursor() as cursor:
        cursor.execute(insert_query, (nome, email, hashed_password, matricula, curso, foto, is_adm))
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

    return user_dict


def get_user_by_email(email):
    select_query = '''
        SELECT * FROM Estudantes WHERE email = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()

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

    update_values = []
    update_fields = []

    if nome is not None:
        update_fields.append('nome')
        update_values.append(nome)
    if email is not None:
        update_fields.append('email')
        update_values.append(email)
    if senha is not None:
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        update_fields.append('senha')
        update_values.append(hashed_password)
    if curso is not None:
        update_fields.append('curso')
        update_values.append(curso)
    if foto is not None:
        update_fields.append('foto')
        update_values.append(foto)
    if is_adm is not None:
        update_fields.append('is_adm')
        update_values.append(is_adm)

    if not update_fields:
        return None

    set_clause = ', '.join([f'{field} = %s' for field in update_fields])

    update_query = f'''
        UPDATE Estudantes
        SET {set_clause}
        WHERE id = %s
        RETURNING id, nome, email, matricula, curso, foto, is_adm
    '''

    update_values.append(user_id)

    with get_cursor() as cursor:
        cursor.execute(update_query, update_values)
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

    return user_dict

def get_users():
    
    select_query = '''
        SELECT id, nome, email, matricula, curso, is_adm, foto FROM Estudantes
    '''
    with get_cursor() as cursor:
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

    return user_list


def get_user_by_id(user_id):

    select_query = '''
        SELECT * FROM Estudantes WHERE id = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()

    if user:
        user_dict = {
            'id': user[0],
            'nome': user[1],
            'email': user[2],
            'matricula': user[4],
            'curso': user[6],
            'is_adm': user[5],
            'foto': base64.b64encode(user[7]).decode('utf-8') if user[7] else None
        }
        return user_dict
    else:
        return None


def delete_user(user_id):

    delete_query = '''
        DELETE FROM Estudantes WHERE id = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(delete_query, (user_id,))

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")
