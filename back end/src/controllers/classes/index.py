from flask import Blueprint, request, jsonify
from src.middlewares.index import check_admin, authenticate_token
from src.services.classes.index import create_class, edit_class, get_classes, get_class_by_id, delete_class

classes_blueprint = Blueprint('turmas', __name__)

@classes_blueprint.route('/turmas', methods=['POST'])
@check_admin
def create_class_controller():
    data = request.get_json()

    turma = data["turma"]
    periodo = data["periodo"]
    professor = data["professor"]
    horario = data["horario"]
    vagas_ocupadas = data["vagas_ocupadas"]
    total_vagas = data["total_vagas"]
    local = data["local"]
    cod_disciplina = data["cod_disciplina"]
    cod_depto = data["cod_depto"]

    class_data = create_class(turma, periodo, professor, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto)
    
    return jsonify(class_data), 201

@classes_blueprint.route('/turmas/<int:class_id>', methods=['PATCH'])
@check_admin
def edit_class_controller(class_id):
    data = request.json

    turma = data.get("turma")
    periodo = data.get("periodo")
    professor = data.get("professor")
    horario = data.get("horario")
    vagas_ocupadas = data.get("vagas_ocupadas")
    total_vagas = data.get("total_vagas")
    local = data.get("local")
    cod_disciplina = data.get("cod_disciplina")
    cod_depto = data.get("cod_depto")

    class_data = edit_class(class_id, turma, periodo, professor, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto)
    
    return jsonify(class_data)


@classes_blueprint.route('/turmas', methods=['GET'])
def get_classes_controller():
    classes = get_classes()
    return jsonify(classes)

@classes_blueprint.route('/turmas/<int:class_id>', methods=['GET'])
def get_class_by_id_controller(class_id):
    class_data = get_class_by_id(class_id)
    if class_data:
        return jsonify(class_data)
    else:
        return jsonify({'message': 'Turma não encontrada'}), 404

@classes_blueprint.route('/turmas/<int:class_id>', methods=['DELETE'])
@check_admin
def delete_class_controller(class_id):
    delete_class(class_id)
    return jsonify({'message': 'Turma excluída com sucesso'})
