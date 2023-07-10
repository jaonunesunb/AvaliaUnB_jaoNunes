from src.db_connection.connection import get_db_connection
import jwt as pyjwt
import base64
import datetime
from dotenv import dotenv_values

env_variables = dotenv_values()

def create_user(nome, email, senha, matricula, curso, foto, is_adm=False):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Estudantes (nome, email, senha, matricula, curso, foto, is_adm)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (nome, email, senha, matricula, curso, foto, is_adm))
    conn.commit()

    cursor.close()
    conn.close()
    
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
    '''

    update_values.append(('user_id', user_id))
    update_values = [value for _, value in update_values]

    cursor.execute(update_query, update_values)
    conn.commit()

    cursor.close()
    conn.close()

def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Estudantes
    '''
    cursor.execute(select_query)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

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

    return user

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
        SELECT id, senha FROM Estudantes WHERE email = %s
    '''
    cursor.execute(select_query, (email,))
    user = cursor.fetchone()

    if user:
        user_id, stored_password = user
        if senha == stored_password:
            token = generate_token(user_id)
            return token

    return None

def generate_token(user_id):
    from flask import current_app

    # Obter a chave secreta da app
    secret_key = current_app.secret_key

    # Configurar payload do token
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Token expira em 2 horas
    }

    # Gerar token JWT
    token = pyjwt.encode(payload, secret_key, algorithm='HS256')

    return token

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")