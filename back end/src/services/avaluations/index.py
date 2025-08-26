from src.db_connection.connection import get_cursor

def create_avaliacao(id_estudante, id_turma, nota, comentario):

    insert_query = '''
        INSERT INTO Avaliacoes (id_estudante, id_turma, nota, comentario)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    '''
    with get_cursor() as cursor:
        cursor.execute(insert_query, (id_estudante, id_turma, nota, comentario))
        avaliacao_id = cursor.fetchone()[0]

    return {
        'id': avaliacao_id,
        'id_estudante': id_estudante,
        'id_turma': id_turma,
        'nota': nota,
        'comentario': comentario
    }

def edit_avaliacao(comentario, nota, avaliacao_id):
    update_query = '''
        UPDATE Avaliacoes
        SET comentario = %s, nota = %s
        WHERE id = %s;
    '''
    with get_cursor() as cursor:
        cursor.execute(update_query, (comentario, nota, avaliacao_id))

    return {
        'id': avaliacao_id,
        'comentario': comentario,
        'nota': nota
    }

def get_avaliacoes():
    select_query = '''
        SELECT * FROM Avaliacoes;
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query)
        avaliacoes = cursor.fetchall()

    return [
        {
            'id': avaliacao[0],
            'id_estudante': avaliacao[1],
            'id_turma': avaliacao[2],
            'comentario': avaliacao[3],
            'nota': avaliacao[4]
        }
        for avaliacao in avaliacoes
    ]

def get_avaliacoes_by_turma_id(turma_id):
    select_query = '''
        SELECT * FROM Avaliacoes WHERE id_turma = %s;
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (turma_id,))
        avaliacoes = cursor.fetchall()

    return [
        {
            'id': avaliacao[0],
            'id_estudante': avaliacao[1],
            'id_turma': avaliacao[2],
            'nota': avaliacao[3],
            'comentario': avaliacao[4]
        }
        for avaliacao in avaliacoes
    ]
    
def get_avaliacoes_by_userID(user_id):
    select_query = '''
        SELECT * FROM Avaliacoes WHERE id_estudante = %s;
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (user_id,))
        avaliacoes = cursor.fetchall()

    return [
        {
            'id': avaliacao[0],
            'id_estudante': avaliacao[1],
            'id_turma': avaliacao[2],
            'nota': avaliacao[3],
            'comentario': avaliacao[4]
        }
        for avaliacao in avaliacoes
    ]

def get_avaliacoes_by_ID(avaliation_id):
    select_query = '''
        SELECT * FROM Avaliacoes WHERE id = %s;
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (avaliation_id,))
        avaliacao = cursor.fetchone()

    return {
        'id': avaliacao[0],
        'id_estudante': avaliacao[1],
        'id_turma': avaliacao[2],
        'nota': avaliacao[3],
        'comentario': avaliacao[4]
    }

def get_all_avaliacoes_same_ID(avaliation_id):
    select_query = '''
        SELECT * FROM Avaliacoes WHERE id = %s;
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (avaliation_id,))
        avaliacoes = cursor.fetchall()

    avaliacoes_list = []
    for avaliacao in avaliacoes:
        avaliacoes_list.append({
            'id': avaliacao[0],
            'id_estudante': avaliacao[1],
            'id_turma': avaliacao[2],
            'nota': avaliacao[3],
            'comentario': avaliacao[4]
        })

    return avaliacoes_list


def delete_avaliacao(avaliacao_id):
    delete_query = '''
        DELETE FROM Avaliacoes WHERE id = %s;
    '''
    with get_cursor() as cursor:
        cursor.execute(delete_query, (avaliacao_id,))
