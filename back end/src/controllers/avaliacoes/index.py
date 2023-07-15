from flask import Blueprint, request, jsonify
from src.middlewares.index import authenticate_token
from src.services.avaluations.index import create_avaliacao, edit_avaliacao, get_avaliacoes, get_avaliacoes_by_turma_id, delete_avaliacao

avaliacoes_blueprint = Blueprint('avaliacoes', __name__)

@avaliacoes_blueprint.route('/avaliacoes', methods=['POST'])
#@authenticate_token
def create_avaliacao_controller():
    id_estudante = request.form.get('id_estudante')
    id_turma = request.form.get('id_turma')
    comentario = request.form.get('comentario')

    if id_estudante and id_turma and comentario:
        avaliacao = create_avaliacao(id_estudante, id_turma, comentario)
        return jsonify(avaliacao), 201
    else:
        return jsonify({"message": "Dados inválidos"}), 400

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['PUT'])
#@authenticate_token
def edit_avaliacao_controller(avaliacao_id):
    data = request.json
    avaliacao = edit_avaliacao(data['comentario'], avaliacao_id)
    return jsonify(avaliacao)

@avaliacoes_blueprint.route('/avaliacoes', methods=['GET'])
#@authenticate_token
def get_avaliacoes_controller():
    avaliacoes = get_avaliacoes()
    return jsonify(avaliacoes)

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['GET'])
#@authenticate_token
def get_avaliacoes_by_turma_id_controller(avaliacao_id):
    avaliacao = get_avaliacoes_by_turma_id(avaliacao_id)
    if avaliacao:
        return jsonify(avaliacao)
    else:
        return jsonify({'message': 'Avaliacao not found'}), 404

@avaliacoes_blueprint.route('/avaliacoes/<int:avaliacao_id>', methods=['DELETE'])
#@authenticate_token
def delete_avaliacao_controller(avaliacao_id):
    delete_avaliacao(avaliacao_id)
    return jsonify({'message': 'Avaliacao deleted successfully'})
