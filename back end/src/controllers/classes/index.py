from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import current_user
from src.services.avaluations.index import get_avaliacoes_by_turma_id
from src.middlewares.index import check_admin, authenticate_token
from src.services.classes.index import create_class, edit_class, get_classes, get_class_by_id, delete_class
from src.services.professors.index import get_professor_by_id
from src.services.disciplines.index import get_disciplina_by_id

classes_blueprint = Blueprint('turmas', __name__)

@classes_blueprint.route('/turmas', methods=['GET'])
def get_classes_controller():
    page = 1  
    per_page = 10  
    class_data = get_classes(page, per_page)
    turmas = []

    for data in class_data:
        print(data)
        disciplina_id = data[8]
        disciplina_obj = get_disciplina_by_id(disciplina_id)
        disciplina = disciplina_obj[1] if disciplina_obj else ''
        turma = {
            'turma': data[1],
            'periodo': data[2],
            'disciplina': disciplina,
            'professor': get_professor_by_id(data[3])[1],
            'horario': data[4],
            'vagas_ocupadas': data[5],
            'total_vagas': data[6],
            'local': data[7],
            'cod_disciplina': data[8],
            'cod_depto': data[9]
        }
        turmas.append(turma)
    
    return render_template('turmas.html', turmas=turmas)

@classes_blueprint.route('/turmas/<int:class_id>', methods=['PATCH'])
#@check_admin
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

@classes_blueprint.route('/turmas/<int:class_id>', methods=['DELETE'])
#@check_admin
def delete_class_controller(class_id):
    delete_class(class_id)
    return jsonify({'message': 'Turma excluída com sucesso'})


@classes_blueprint.route('/turmas/<int:turma_id>', methods=['GET'])
def get_class_details_controller(turma_id):
    turma = get_class_by_id(turma_id)
    avaliacoes = get_avaliacoes_by_turma_id(turma_id)
    return render_template('turmasDetails.html', turma=turma, avaliacoes=avaliacoes, current_user=current_user)

@classes_blueprint.route('/turmas/<int:class_id>', methods=['GET'])
def get_class_by_id_controller(class_id):
    class_data = get_class_by_id(class_id)
    if class_data:
        return jsonify(class_data)
    else:
        return jsonify({'message': 'Turma não encontrada'}), 404
