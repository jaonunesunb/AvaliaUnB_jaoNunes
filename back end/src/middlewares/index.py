from functools import wraps
import os
import jwt
from flask import g, request, jsonify

def authenticate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = g.get('token')

        if not token:
            return jsonify({'message': 'Token não fornecido'}), 401

        try:
            secret_key = os.getenv('SECRET_KEY')
            print('Token:', token)  # Imprimir o token para verificar se está sendo recebido corretamente
            print('Secret Key:', secret_key)  # Imprimir a chave secreta para verificar se está configurada corretamente

            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
            print('Decoded Token:', decoded_token)  # Imprimir o token decodificado para verificar seu conteúdo

            user_id = decoded_token['user_id']
            is_admin = decoded_token['is_admin']

            request.current_user = {
                'user_id': user_id,
                'is_admin': is_admin
            }
            print("Middleware", func(*args, **kwargs))
            return func(*args, **kwargs)
        except jwt.DecodeError as e:
            print('DecodeError:', e)  # Imprimir a exceção DecodeError para verificar a causa do erro
            return jsonify({'message': 'Token inválido'}), 401
        except jwt.ExpiredSignatureError as e:
            print('ExpiredSignatureError:', e)  # Imprimir a exceção ExpiredSignatureError para verificar a causa do erro
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError as e:
            print('InvalidTokenError:', e)  # Imprimir a exceção InvalidTokenError para verificar a causa do erro
            return jsonify({'message': 'Token inválido'}), 401

    return wrapper


def check_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = g.get('token')

        if not token:
            return jsonify({'message': 'Token não fornecido'}), 401

        is_admin = request.headers.get('X-Is-Admin')
        if not is_admin:
            return jsonify({'message': 'Acesso negado. Este recurso requer privilégios de administrador.'}), 403

        return func(*args, **kwargs)

    return wrapper
