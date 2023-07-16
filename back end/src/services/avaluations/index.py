from src.db_connection.connection import get_db_connection

def create_avaliacao(id_estudante, id_turma, nota, comentario):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Avaliacoes (id_estudante, id_turma, nota, comentario)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    '''
    cursor.execute(insert_query, (id_estudante, id_turma, nota, comentario))
    avaliacao_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return {
        'id': avaliacao_id,
        'id_estudante': id_estudante,
        'id_turma': id_turma,
        'nota': nota,
        'comentario': comentario
    }

def edit_avaliacao(comentario, avaliacao_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_query = '''
        UPDATE Avaliacoes
        SET comentario = %s
        WHERE id = %s;
    '''
    cursor.execute(update_query, (comentario, avaliacao_id))
    conn.commit()

    cursor.close()
    conn.close()

    return {
        'id': avaliacao_id,
        'comentario': comentario
    }

def edit_avaliacao(comentario, avaliacao_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_query = '''
        UPDATE Avaliacoes
        SET comentario = %s
        WHERE id = %s;
    '''
    cursor.execute(update_query, (comentario, avaliacao_id))
    conn.commit()

    cursor.close()
    conn.close()

    return {
        'id': avaliacao_id,
        'comentario': comentario
    }
    
def get_avaliacoes():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Avaliacoes;
    '''
    cursor.execute(select_query)
    avaliacoes = cursor.fetchall()

    cursor.close()
    conn.close()

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
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Avaliacoes WHERE id_turma = %s;
    '''
    cursor.execute(select_query, (turma_id,))
    avaliacoes = cursor.fetchall()

    cursor.close()
    conn.close()

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
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Avaliacoes WHERE id_estudante = %s;
    '''
    cursor.execute(select_query, (user_id,))
    avaliacoes = cursor.fetchall()

    cursor.close()
    conn.close()

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

def delete_avaliacao(avaliacao_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    delete_query = '''
        DELETE FROM Avaliacoes WHERE id = %s;
    '''
    cursor.execute(delete_query, (avaliacao_id,))
    conn.commit()

    cursor.close()
    conn.close()
