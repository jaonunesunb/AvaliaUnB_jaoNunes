from functools import wraps
import os
import jwt
from flask import request, jsonify

def authenticate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        secret_key = os.getenv('SECRET_KEY')

        if not authorization_header:
            return jsonify({'message': 'Token não fornecido'}), 401

        try:
            token_type, token = authorization_header.split(' ')
            if token_type != 'Bearer':
                return jsonify({'message': 'Token inválido'}), 401

            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

            return func(*args, **kwargs)

        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

    return wrapper

def check_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verificar se o usuário está autenticado
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return jsonify({'message': 'Token não fornecido'}), 401

        try:
            token_type, token = authorization_header.split(' ')
            if token_type != 'Bearer':
                return jsonify({'message': 'Token inválido'}), 401

            secret_key = os.getenv('SECRET_KEY')
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

            # Verificar se o usuário é um administrador
            is_admin = decoded_token.get('is_adm')
            if not is_admin:
                return jsonify({'message': 'Acesso negado. Este recurso requer privilégios de administrador.'}), 403

            return func(*args, **kwargs)

        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

    return wrapper