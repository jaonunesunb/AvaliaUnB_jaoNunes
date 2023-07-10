from src.db_connection.connection import get_db_connection

from src.db_connection.connection import get_db_connection

def create_professor(nome, departamento):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_departamento_query = "SELECT id FROM Departamentos WHERE id = %s"
    cursor.execute(select_departamento_query, (departamento,))
    departamento_exists = cursor.fetchone()

    if not departamento_exists:
        cursor.close()
        conn.close()
        return None  

    insert_query = "INSERT INTO Professores (nome, departamento_id) VALUES (%s, %s) RETURNING id, nome, departamento_id"
    cursor.execute(insert_query, (nome, departamento))
    professor = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return professor

def get_professor_by_id(professor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = "SELECT * FROM Professores WHERE id = %s"
    cursor.execute(select_query, (professor_id,))
    professor = cursor.fetchone()
    cursor.close()
    conn.close()
    return professor

def get_all_professores():
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = "SELECT * FROM Professores"
    cursor.execute(select_query)
    professores = cursor.fetchall()
    cursor.close()
    conn.close()
    return professores

def update_professor(professor_id, nome=None, departamento=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if departamento is not None:
        
        select_departamento_query = "SELECT id FROM Departamentos WHERE id = %s"
        cursor.execute(select_departamento_query, (departamento,))
        departamento_exists = cursor.fetchone()

        if not departamento_exists:
            cursor.close()
            conn.close()
            return None  

    update_query = "UPDATE Professores SET"
    update_values = []

    if nome is not None:
        update_query += " nome = %s,"
        update_values.append(nome)

    if departamento is not None:
        update_query += " departamento_id = %s,"
        update_values.append(departamento)

    update_query = update_query.rstrip(',')

    update_query += " WHERE id = %s"
    update_values.append(professor_id)

    cursor.execute(update_query, tuple(update_values))
    conn.commit()

    select_query = "SELECT * FROM Professores WHERE id = %s"
    cursor.execute(select_query, (professor_id,))
    updated_professor = cursor.fetchone()

    cursor.close()
    conn.close()

    return updated_professor


def delete_professor(professor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    delete_query = "DELETE FROM Professores WHERE id = %s"
    cursor.execute(delete_query, (professor_id,))
    conn.commit()
    cursor.close()
    conn.close()
