import psycopg2
from flask import Blueprint, jsonify, render_template
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

    conn.commit()

    cursor.close()
    conn.close()

@views_bp.route('/ranking')
def visualizar_views_controller():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query_melhores_notas = '''
    SELECT id, turma, media_notas
    FROM TurmasMelhoresNotas
'''
    cursor.execute(select_query_melhores_notas)
    rows_melhores_notas = cursor.fetchall()
    columns_melhores_notas = [desc[0] for desc in cursor.description]
    turmas_melhores_notas = [
        {column: round(value, 2) if isinstance(value, float) else value for column, value in zip(columns_melhores_notas, row)}
        for row in rows_melhores_notas
    ]

    select_query_piores_notas = '''
        SELECT id, turma, media_notas
        FROM TurmasPioresNotas
    '''
    cursor.execute(select_query_piores_notas)
    rows_piores_notas = cursor.fetchall()
    columns_piores_notas = [desc[0] for desc in cursor.description]
    turmas_piores_notas = [
        {column: round(value, 2) if isinstance(value, float) else value for column, value in zip(columns_piores_notas, row)}
        for row in rows_piores_notas
    ]
    cursor.close()
    conn.close()

    return render_template('ranking.html', turmas_melhores_notas=turmas_melhores_notas, turmas_piores_notas=turmas_piores_notas)

views_denuncias = Blueprint("views_denuncias", __name__, url_prefix="/views")
def create_denuncias_views():
    conn = get_db_connection()
    cursor = conn.cursor()
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


