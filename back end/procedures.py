from flask import Blueprint, jsonify, request
from src.db_connection.connection import execute_query, execute_query_with_result, get_db_connection

procedures_bp = Blueprint("procedures_bp", __name__, url_prefix="/procedures")

def create_calcular_quantidade_denuncias_nao_resolvidas():
    query = """
        CREATE OR REPLACE FUNCTION calcular_quantidade_denuncias_nao_resolvidas()
          RETURNS INTEGER AS $$
        BEGIN
          RETURN (
            SELECT COUNT(*)
            FROM Denuncias
            WHERE avaliada = FALSE
          );
        END;
        $$ LANGUAGE plpgsql;
    """
    execute_query(query)

def create_calcular_quantidade_denuncias_resolvidas():
    query = """
        CREATE OR REPLACE FUNCTION calcular_quantidade_denuncias_resolvidas()
          RETURNS INTEGER AS $$
        BEGIN
          RETURN (
            SELECT COUNT(*)
            FROM Denuncias
            WHERE avaliada = TRUE
          );
        END;
        $$ LANGUAGE plpgsql;
    """
    execute_query(query)

def create_verificar_avaliacao_estudante_turma():
    query = """
        CREATE OR REPLACE FUNCTION verificar_avaliacao_estudante_turma(id_estudante INTEGER, id_turma INTEGER)
          RETURNS BOOLEAN AS $$
        BEGIN
          RETURN EXISTS (
            SELECT 1
            FROM Avaliacoes
            WHERE id_estudante = $1
              AND id_turma = $2
          );
        END;
        $$ LANGUAGE plpgsql;
    """
    execute_query(query)

def create_procedures():
    create_calcular_quantidade_denuncias_nao_resolvidas()
    create_calcular_quantidade_denuncias_resolvidas()
    create_verificar_avaliacao_estudante_turma()

@procedures_bp.route("/denuncias-nao-resolvidas", methods=["GET"])
def get_quantidade_denuncias_nao_resolvidas():
    query = "SELECT calcular_quantidade_denuncias_nao_resolvidas();"
    result = execute_query_with_result(query)
    quantidade = result[0][0]
    return jsonify({"quantidade": quantidade})

@procedures_bp.route("/denuncias-resolvidas", methods=["GET"])
def get_quantidade_denuncias_resolvidas():
    query = "SELECT calcular_quantidade_denuncias_resolvidas();"
    result = execute_query_with_result(query)
    quantidade = result[0][0]
    return jsonify({"quantidade": quantidade})

@procedures_bp.route("/verificar-avaliacao", methods=["GET"])
def verificar_avaliacao():
    id_estudante = request.args.get("id_estudante")
    id_turma = request.args.get("id_turma")
    if id_estudante and id_turma:
        query = "SELECT verificar_avaliacao_estudante_turma(%s, %s);"
        args = (id_estudante, id_turma)
        result = execute_query_with_result(query, args)
        existe_avaliacao = result[0][0]
        return jsonify({"existe_avaliacao": existe_avaliacao})
    else:
        return jsonify({"message": "Parâmetros inválidos"}), 400
