from src.db_connection.connection import get_db_connection

def create_avaliacao(id_estudante, id_turma, comentario):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Avaliacoes (id_estudante, id_turma, comentario)
        VALUES (%s, %s, %s)
        RETURNING id;
    '''
    cursor.execute(insert_query, (id_estudante, id_turma, comentario))
    avaliacao_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return {
        'id': avaliacao_id,
        'id_estudante': id_estudante,
        'id_turma': id_turma,
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

    return [dict(avaliacao) for avaliacao in avaliacoes]

def get_avaliacao_by_id(avaliacao_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Avaliacoes WHERE id = %s;
    '''
    cursor.execute(select_query, (avaliacao_id,))
    avaliacao = cursor.fetchone()

    cursor.close()
    conn.close()

    if avaliacao:
        return dict(avaliacao)
    else:
        return None

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
