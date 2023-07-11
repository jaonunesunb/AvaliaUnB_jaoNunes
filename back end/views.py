import psycopg2
from flask import Blueprint, jsonify
from src.db_connection.connection import get_db_connection

views_bp = Blueprint("views_bp", __name__, url_prefix="/views")

def create_views():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Criação da view TurmasMelhoresNotas
    create_view_turmas_melhores_notas_query = '''
        CREATE OR REPLACE VIEW TurmasMelhoresNotas AS
        SELECT Turmas.id, Turmas.turma, AVG(Avaliacoes.nota) AS media_notas
        FROM Turmas
        INNER JOIN Avaliacoes ON Turmas.id = Avaliacoes.id_turma
        GROUP BY Turmas.id, Turmas.turma
        ORDER BY media_notas DESC;
    '''
    cursor.execute(create_view_turmas_melhores_notas_query)

    # Criação da view TurmasPioresNotas
    create_view_turmas_piores_notas_query = '''
        CREATE OR REPLACE VIEW TurmasPioresNotas AS
        SELECT Turmas.id, Turmas.turma, AVG(Avaliacoes.nota) AS media_notas
        FROM Turmas
        INNER JOIN Avaliacoes ON Turmas.id = Avaliacoes.id_turma
        GROUP BY Turmas.id, Turmas.turma
        ORDER BY media_notas ASC;
    '''
    cursor.execute(create_view_turmas_piores_notas_query)

    # Criação da view DenunciasResolvidas
    create_view_denuncias_resolvidas_query = '''
        CREATE OR REPLACE VIEW DenunciasResolvidas AS
        SELECT Denuncias.id, Denuncias.motivo, Avaliacoes.comentario
        FROM Denuncias
        INNER JOIN Avaliacoes ON Denuncias.id_avaliacao = Avaliacoes.id
        WHERE Denuncias.avaliada = TRUE;
    '''
    cursor.execute(create_view_denuncias_resolvidas_query)

    # Criação da view DenunciasNaoResolvidas
    create_view_denuncias_nao_resolvidas_query = '''
        CREATE OR REPLACE VIEW DenunciasNaoResolvidas AS
        SELECT Denuncias.id, Denuncias.motivo, Avaliacoes.comentario
        FROM Denuncias
        INNER JOIN Avaliacoes ON Denuncias.id_avaliacao = Avaliacoes.id
        WHERE Denuncias.avaliada = FALSE;
    '''
    cursor.execute(create_view_denuncias_nao_resolvidas_query)

    conn.commit()

    cursor.close()
    conn.close()

# Endpoint para verificar se as views foram criadas
@views_bp.route("/verificar-views", methods=["GET"])
def verificar_views():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificação da existência da view TurmasMelhoresNotas
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'turmasmelhoresnotas')")
    turmas_melhores_notas_exists = cursor.fetchone()[0]

    # Verificação da existência da view TurmasPioresNotas
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'turmaspioresnotas')")
    turmas_piores_notas_exists = cursor.fetchone()[0]

    # Verificação da existência da view DenunciasResolvidas
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'denunciasresolvidas')")
    denuncias_resolvidas_exists = cursor.fetchone()[0]

    # Verificação da existência da view DenunciasNaoResolvidas
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'denunciasnaoresolvidas')")
    denuncias_nao_resolvidas_exists = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    result = {
        "TurmasMelhoresNotas": turmas_melhores_notas_exists,
        "TurmasPioresNotas": turmas_piores_notas_exists,
        "DenunciasResolvidas": denuncias_resolvidas_exists,
        "DenunciasNaoResolvidas": denuncias_nao_resolvidas_exists
    }

    return jsonify(result)