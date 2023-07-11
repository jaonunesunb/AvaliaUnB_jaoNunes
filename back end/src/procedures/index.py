from flask import Blueprint, jsonify, request
from src.db_connection.connection import execute_query_with_result

procedures_bp = Blueprint("procedures_bp", __name__, url_prefix="/procedures")

def calcular_quantidade_denuncias_nao_resolvidas():
    query = "SELECT COUNT(*) FROM Denuncias WHERE avaliada = FALSE;"
    result = execute_query_with_result(query)
    return result[0][0]

def calcular_quantidade_denuncias_resolvidas():
    query = "SELECT COUNT(*) FROM Denuncias WHERE avaliada = TRUE;"
    result = execute_query_with_result(query)
    return result[0][0]

def verificar_avaliacao_estudante_turma(id_estudante, id_turma):
    query = "SELECT EXISTS (SELECT 1 FROM Avaliacoes WHERE id_estudante = %s AND id_turma = %s);"
    args = (id_estudante, id_turma)
    result = execute_query_with_result(query, args)
    return result[0][0]

@procedures_bp.route("/denuncias-nao-resolvidas", methods=["GET"])
def get_quantidade_denuncias_nao_resolvidas():
    quantidade = calcular_quantidade_denuncias_nao_resolvidas()
    return jsonify({"quantidade": quantidade})
 
@procedures_bp.route("/denuncias-resolvidas", methods=["GET"])
def get_quantidade_denuncias_resolvidas():
    quantidade = calcular_quantidade_denuncias_resolvidas()
    return jsonify({"quantidade": quantidade})

@procedures_bp.route("/verificar-avaliacao", methods=["GET"])
def verificar_avaliacao():
    id_estudante = request.args.get("id_estudante")
    id_turma = request.args.get("id_turma")
    if id_estudante and id_turma:
        existe_avaliacao = verificar_avaliacao_estudante_turma(id_estudante, id_turma)
        return jsonify({"existe_avaliacao": existe_avaliacao})
    else:
        return jsonify({"message": "Parâmetros inválidos"}), 400
