from flask import Blueprint, request, jsonify
from src.middlewares.index import check_admin, authenticate_token
from src.services.departamentos.index import create_departamento, get_departamentos, get_departamento_by_id

departamento_blueprint = Blueprint('departamento', __name__)

@departamento_blueprint.route('/departamentos', methods=['POST'])
@check_admin
def create_departamento_controller():
    data = request.get_json()
    nome = data["nome"]

    departamento = create_departamento(nome)

    return jsonify(departamento), 201

@departamento_blueprint.route('/departamentos', methods=['GET'])
@authenticate_token
def get_departamentos_controller():
    departamentos = get_departamentos()
    return jsonify(departamentos)

@departamento_blueprint.route('/departamentos/<int:departamento_id>', methods=['GET'])
@authenticate_token
def get_departamento_by_id_controller(departamento_id):
    departamento = get_departamento_by_id(departamento_id)
    if departamento:
        return jsonify(departamento)
    else:
        return jsonify({'message': 'Departamento não encontrado'}), 404

