from flask import Blueprint, jsonify, request
from src.db_connection.connection import get_db_connection
from src.middlewares.index import authenticate_token, check_admin
from src.services.professors.index import create_professor, get_professor_by_id, get_all_professores, update_professor, delete_professor

professors_blueprint = Blueprint('professors', __name__)

@professors_blueprint.route('/professors', methods=['POST'])
@check_admin
def create_professor_controller():
    data = request.get_json()
    nome = data['nome']
    departamento = data['departamento_id']

    professor = create_professor(nome, departamento)

    if professor:
        return jsonify(professor), 200
    else:
        return jsonify({'message': 'Erro ao criar professor'}), 500

@professors_blueprint.route('/professors/<int:professor_id>', methods=['GET'])
@authenticate_token
def get_professor_by_id_controller(professor_id):
    professor = get_professor_by_id(professor_id)

    if professor:
        return jsonify(professor), 200
    else:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professors_blueprint.route('/professors', methods=['GET'])
@authenticate_token
def get_all_professores_controller():
    professores = get_all_professores()

    return jsonify(professores), 200

@professors_blueprint.route('/professors/<int:professor_id>', methods=['PATCH'])
@check_admin
def update_professor_controller(professor_id):
    data = request.get_json()
    nome = data.get('nome')
    departamento = data.get('departamento')

    updated_professor = update_professor(professor_id, nome, departamento)

    if updated_professor:
        return jsonify(updated_professor), 200
    else:
        return jsonify({'message': 'Erro ao atualizar professor'}), 500

@professors_blueprint.route('/professors/<int:professor_id>', methods=['DELETE'])
@check_admin
def delete_professor_controller(professor_id):
    delete_professor(professor_id)
    return jsonify({'message': 'Professor deletado com sucesso'}), 200
