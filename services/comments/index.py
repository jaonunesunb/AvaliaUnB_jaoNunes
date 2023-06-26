from db_connection.connection import get_db_connection

def create_comment(id_estudante, id_turma, comentario):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Avaliacoes (id_estudante, id_turma, comentario)
        VALUES (%s, %S, %s);
    '''
    cursor.execute(insert_query, (id_estudante, id_turma, comentario))
    conn.commit()

    conn.commit()
    cursor.close()
    conn.close()
    
def edit_comment(comentario, comentario_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_query = '''
        UPDATE Avaliacoes
        SET comentario = %s
        WHERE id = %s
    '''
    cursor.execute(update_query, (comentario, comentario_id))
    conn.commit()

    cursor.close()
    conn.close()

def get_comments():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Avaliacoes
    '''
    cursor.execute(select_query)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

def get_comment_by_id(comentario_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Avaliacoes WHERE id = %s
    '''
    cursor.execute(select_query, (comentario_id))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def delete_comment(comentario_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    delete_query = '''
        DELETE FROM Avaliacoes WHERE id = %s
    '''
    cursor.execute(delete_query, (comentario_id,))
    conn.commit()

    cursor.close()
    conn.close()
