import math
from flask import Blueprint, g, jsonify, request, render_template
from src.db_connection.connection import get_db_connection
from src.middlewares.index import check_admin
from src.services.professors.index import create_professor, get_professor_by_id, get_all_professores, update_professor, delete_professor
from src.services.departamentos.index import get_departamento_name

professors_blueprint = Blueprint('professores', __name__)

@professors_blueprint.route('/professores', methods=['POST'])
@check_admin(True)
def create_professor_controller():
    data = request.get_json()
    nome = data['nome']
    departamento = data['departamento_id']

    professor = create_professor(nome, departamento)

    if professor:
        return jsonify(professor), 200
    else:
        return jsonify({'message': 'Erro ao criar professor'}), 500

@professors_blueprint.route('/professores/<int:professor_id>', methods=['GET'])
def get_professor_by_id_controller(professor_id):
    professor = get_professor_by_id(professor_id)

    if professor:
        return jsonify(professor), 200
    else:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professors_blueprint.route('/professores', methods=['GET'])
def view_professors():
    page = int(request.args.get('page', 1))
    per_page = 10
    professor_data = get_all_professores(page, per_page)
    professores = professor_data['professores']
    total_pages = professor_data['total_pages']
    current_page = professor_data['current_page']
    previous_page = professor_data['previous_page']
    next_page = professor_data['next_page']
    pages = professor_data['pages']
    is_admin = g.get('is_admin')

    template_data = {
        'professores': professores,
        'is_admin': is_admin,
        'total_pages': total_pages,
        'current_page': current_page,
        'previous_page': previous_page,
        'next_page': next_page,
        'pages': pages
    }

    return render_template('professorsPage.html', **template_data)

@professors_blueprint.route('/professores/<int:professor_id>', methods=['PUT'])
#@check_admin
def update_professor_controller(professor_id):
    data = request.get_json()
    nome = data.get('nome')
    departamento = data.get('departamento')

    updated_professor = update_professor(professor_id, nome, departamento)

    if updated_professor:
        return jsonify(updated_professor), 200
    else:
        return jsonify({'message': 'Erro ao atualizar professor'}), 500

@professors_blueprint.route('/professores/<int:professor_id>', methods=['DELETE'])
#@check_admin
def delete_professor_controller(professor_id):
    delete_professor(professor_id)
    return jsonify({'message': 'Professor deletado com sucesso'}), 200

professors_blueprint = Blueprint('professors', __name__)


@professors_blueprint.route('/professors', methods=['GET'])
def view_professors():
    page = int(request.args.get('page', 1)) 
    per_page = 10  
    professor_data = get_all_professores(page, per_page)['professores']  
    professores = []
    
    for data in professor_data:
        professor = {
            'id': data['id'],
            'nome': data['nome'],
            'departamento': get_departamento_name(data['departamento_id'])
        }
        professores.append(professor)
    
    total_pages = math.ceil(len(professor_data) / per_page)  
    pages = range(1, total_pages + 1)  

    return render_template('professorsPage.html', professores=professores, total_pages=total_pages, current_page=page, pages=pages)