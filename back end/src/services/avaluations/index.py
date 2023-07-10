from src.db_connection.connection import get_db_connection

def create_avaliacao(id_estudante, id_turma, comentario):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Avaliacoes (id_estudante, id_turma, comentario)
        VALUES (%s, %s, %s);
    '''
    cursor.execute(insert_query, (id_estudante, id_turma, comentario))
    conn.commit()

    cursor.close()
    conn.close()

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

    return avaliacoes

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

    return avaliacao

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
