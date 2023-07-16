from flask import Blueprint, request, jsonify
from src.middlewares.index import authenticate_token
from flask_login import login_required
from src.services.avaluations.index import create_avaliacao, edit_avaliacao, get_avaliacoes, get_avaliacoes_by_turma_id, delete_avaliacao, get_avaliacoes_by_userID

avaliacoes_blueprint = Blueprint('avaliacoes', __name__)

@avaliacoes_blueprint.route('/avaliacoes', methods=['POST'])
#@authenticate_token
@login_required
def create_avaliacao_controller():
    id_estudante = request.form['id_estudante']
    id_turma = request.form['id_turma']
    nota = request.form['nota']
    comentario = request.form['comentario']
    
    if id_estudante and id_turma and nota and comentario:
        avaliacao = create_avaliacao(id_estudante, id_turma, nota, comentario)
        return jsonify(avaliacao), 201
    else:
        return jsonify({"message": "Dados inválidos"}), 400


@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['PUT'])
#@authenticate_token
@login_required
def edit_avaliacao_controller(avaliacao_id):
    data = request.json
    avaliacao = edit_avaliacao(data['comentario'], avaliacao_id)
    return jsonify(avaliacao)

@avaliacoes_blueprint.route('/avaliacoes', methods=['GET'])
def get_avaliacoes_controller():
    avaliacoes = get_avaliacoes()
    return jsonify(avaliacoes)

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['GET'])
def get_avaliacoes_by_turma_id_controller(avaliacao_id):
    avaliacao = get_avaliacoes_by_turma_id(avaliacao_id)
    if avaliacao:
        return jsonify(avaliacao)
    else:
        return jsonify({'message': 'Avaliacao not found'}), 404

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['GET'])
def get_avaliacoes_by_userID_controller(user_id):
    avaliacao = get_avaliacoes_by_userID(user_id)
    if avaliacao:
        return jsonify(avaliacao)
    else:
        return jsonify({'message': 'Avaliacao not found'}), 404


@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['DELETE'])
#@authenticate_token
@login_required
def delete_avaliacao_controller(avaliacao_id):
    delete_avaliacao(avaliacao_id)
    return jsonify({'message': 'Avaliacao deleted successfully'})
