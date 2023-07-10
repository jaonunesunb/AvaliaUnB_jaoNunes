from urllib import request
from dotenv import dotenv_values
import jwt as pyjwt
from flask import request, jsonify, current_app
from src.db_connection.connection import get_db_connection

env_variables = dotenv_values()


def ensure_admin_and_fields():
    route = request.path
    # Rotas que não requerem autenticação
    excluded_routes = ['/users/login', '/users/register']

    if route in excluded_routes:
        return None

    token = request.headers.get('Authorization')

    secret_key = current_app.secret_key
    decoded_token = pyjwt.decode(token, secret_key, algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    if not user_id:
        return jsonify({'message': 'Invalid token.'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = "SELECT is_admin, email, password FROM Estudantes WHERE id = %s"
    cursor.execute(select_query, (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'User not found.'}), 409
    
    is_admin = user[0]
    email = user[1]
    password = user[2]

    if not is_admin or not email or not password:
        return jsonify({'message': 'Insufficient permissions.'}), 403

    cursor.close()
    conn.close()

    return None
