from flask import jsonify, Blueprint, request
from src.services.disciplines.index import (
    create_disciplina,
    get_disciplina_by_id,
    get_all_disciplinas,
    update_disciplina,
    delete_disciplina
)

disciplinas_blueprint = Blueprint('disciplinas', __name__)

@disciplinas_blueprint.route('/disciplinas', methods=['POST'])
def create_disciplina_controller():
    nome = request.json['nome']
    departamento = request.json['departamento']

    create_disciplina(nome, departamento)

    return jsonify(message='Disciplina criada com sucesso'), 201

@disciplinas_blueprint.route('/disciplinas/<disciplina_id>', methods=['GET'])
def get_disciplina_by_id_controller(disciplina_id):
    disciplina = get_disciplina_by_id(disciplina_id)

    if disciplina:
        return jsonify(disciplina), 200
    else:
        return jsonify(message='Disciplina não encontrada'), 404

@disciplinas_blueprint.route('/disciplinas', methods=['GET'])
def get_all_disciplinas_controller():
    disciplinas = get_all_disciplinas()

    return jsonify(disciplinas), 200

@disciplinas_blueprint.route('/disciplinas/<disciplina_id>', methods=['PUT'])
def update_disciplina_controller(disciplina_id):
    departamento = request.json['departamento']

    disciplina = get_disciplina_by_id(disciplina_id)

    if disciplina:
        update_disciplina(disciplina_id, departamento)
        return jsonify(message='Disciplina atualizada com sucesso'), 200
    else:
        return jsonify(message='Disciplina não encontrada'), 404

@disciplinas_blueprint.route('/disciplinas/<disciplina_id>', methods=['DELETE'])
def delete_disciplina_controller(disciplina_id):
    disciplina = get_disciplina_by_id(disciplina_id)

    if disciplina:
        delete_disciplina(disciplina_id)
        return jsonify(message='Disciplina excluída com sucesso'), 200
    else:
        return jsonify(message='Disciplina não encontrada'), 404
