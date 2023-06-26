from db_connection.connection import get_db_connection

def create_user(nome, email, senha, matricula, curso):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Estudantes (nome, email, senha, matricula, curso)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (nome, email, senha, matricula, curso))
    conn.commit()

    cursor.close()
    conn.close()
    
def edit_user(user_id, nome=None, email=None, senha=None, curso=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_values = []

    if nome is not None:
        update_values.append(('nome', nome))
    if email is not None:
        update_values.append(('email', email))
    if senha is not None:
        update_values.append(('senha', senha))
    if curso is not None:
        update_values.append(('curso', curso))

    set_clause = ', '.join([f'{field} = %s' for field, _ in update_values])

    update_query = f'''
        UPDATE Estudantes
        SET {set_clause}
        WHERE id = %s
    '''

    update_values.append(('user_id', user_id))
    update_values = [value for _, value in update_values]

    cursor.execute(update_query, update_values)
    conn.commit()

    cursor.close()
    conn.close()


def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Estudantes
    '''
    cursor.execute(select_query)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Estudantes WHERE id = %s
    '''
    cursor.execute(select_query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    delete_query = '''
        DELETE FROM Estudantes WHERE id = %s
    '''
    cursor.execute(delete_query, (user_id,))
    conn.commit()

    cursor.close()
    conn.close()
