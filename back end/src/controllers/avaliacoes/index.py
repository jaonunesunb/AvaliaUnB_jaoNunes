from flask import Blueprint, request, jsonify
from src.middlewares.index import authenticate_token
from src.services.avaluations.index import create_avaliacao, edit_avaliacao, get_avaliacoes, get_avaliacao_by_id, delete_avaliacao

avaliacoes_blueprint = Blueprint('avaliacoes', __name__)

@avaliacoes_blueprint.route('/avaliacoes', methods=['POST'])
@authenticate_token
def create_avaliacao_controller():
    data = request.json
    create_avaliacao(data['id_estudante'], data['id_turma'], data['comentario'])
    return jsonify('Avaliacao created successfully'), 201

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['PUT'])
@authenticate_token
def edit_avaliacao_controller(avaliacao_id):
    data = request.json
    edit_avaliacao(data['comentario'], avaliacao_id)
    return jsonify('Avaliacao updated successfully')

@avaliacoes_blueprint.route('/avaliacoes', methods=['GET'])
@authenticate_token
def get_avaliacoes_controller():
    avaliacoes = get_avaliacoes()
    return jsonify(avaliacoes)

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['GET'])
@authenticate_token
def get_avaliacao_by_id_controller(avaliacao_id):
    avaliacao = get_avaliacao_by_id(avaliacao_id)
    return jsonify(avaliacao)

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['DELETE'])
@authenticate_token
def delete_avaliacao_controller(avaliacao_id):
    delete_avaliacao(avaliacao_id)
    return jsonify({'message': 'Avaliacao deleted successfully'})
