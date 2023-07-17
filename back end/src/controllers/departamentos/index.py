from flask import Blueprint, request, jsonify, render_template
from src.middlewares.index import check_admin, is_authenticated
from src.services.departamentos.index import create_departamento, get_departamentos, get_departamento_by_id

departamento_blueprint = Blueprint('departamento', __name__)

@departamento_blueprint.route('/departamentos', methods=['POST'])
@check_admin(True)
def create_departamento_controller():
    data = request.get_json()
    nome = data["nome"]

    departamento = create_departamento(nome)

    return jsonify(departamento), 201

@departamento_blueprint.route('/departaments', methods=['GET'])
def view_departamentos():
    departamentos = get_departamentos()
    return render_template('departamentosPage.html', departamentos=departamentos)

@departamento_blueprint.route('/departamentos/<int:departamento_id>', methods=['GET'])
@is_authenticated
def get_departamento_by_id_controller(departamento_id):
    departamento = get_departamento_by_id(departamento_id)
    if departamento:
        return jsonify(departamento)
    else:
        return jsonify({'message': 'Departamento não encontrado'}), 404

@departamento_blueprint.route('/departamentos', methods=['GET'])
def view_departamentos_controller():
    departamentos = get_departamentos()
    return render_template('departamentosPage.html', departamentos=departamentos)