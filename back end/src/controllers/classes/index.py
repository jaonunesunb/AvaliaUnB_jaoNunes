from flask import Blueprint, request, jsonify
from src.services.classes.index import create_class, edit_class, get_classes, get_class_by_id, delete_class

classes_blueprint = Blueprint('classes', __name__)

@classes_blueprint.route('/classes', methods=['POST'])
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

    create_class(turma, periodo, professor, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto)
    
    return jsonify({"message": "Turma criada com sucesso"}), 201

@classes_blueprint.route('/classes/<int:class_id>', methods=['PUT'])
def edit_class_controller(class_id):
    data = request.json
    turma = data["turma"]
    periodo = data["periodo"]
    professor = data["professor"]
    horario = data["horario"]
    vagas_ocupadas = data["vagas_ocupadas"]
    total_vagas = data["total_vagas"]
    local = data["local"]
    cod_disciplina = data["cod_disciplina"]
    cod_depto = data["cod_depto"]

    edit_class(class_id, turma, periodo, professor, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto)
    
    return jsonify('Turma atualizada com sucesso')

@classes_blueprint.route('/classes', methods=['GET'])
def get_classes_controller():
    classes = get_classes()
    return jsonify(classes)

@classes_blueprint.route('/classes/<int:class_id>', methods=['GET'])
def get_class_by_id_controller(class_id):
    class_data = get_class_by_id(class_id)
    if class_data:
        return jsonify(class_data)
    else:
        return jsonify({'message': 'Turma não encontrada'}), 404

@classes_blueprint.route('/classes/<int:class_id>', methods=['DELETE'])
def delete_class_controller(class_id):
    delete_class(class_id)
    return jsonify({'message': 'Turma excluída com sucesso'})
