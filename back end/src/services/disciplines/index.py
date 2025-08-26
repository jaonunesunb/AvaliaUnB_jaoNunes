from src.db_connection.connection import get_cursor

def create_disciplina(nome, departamento):
    insert_query = "INSERT INTO Disciplinas (nome, departamento) VALUES (%s, %s)"
    with get_cursor() as cursor:
        cursor.execute(insert_query, (nome, departamento))

def get_disciplina_by_id(disciplina_id):
    select_query = "SELECT * FROM Disciplinas WHERE codigo = %s::text"
    with get_cursor() as cursor:
        cursor.execute(select_query, (disciplina_id,))
        disciplina = cursor.fetchone()
    if disciplina is None:
        return None
    else:
        return disciplina


def get_all_disciplinas():
    select_query = "SELECT * FROM Disciplinas"
    with get_cursor() as cursor:
        cursor.execute(select_query)
        disciplinas = cursor.fetchall()
    return disciplinas

def update_disciplina(disciplina_id, departamento):
    update_query = "UPDATE Disciplinas SET departamento = %s WHERE codigo = %s"
    with get_cursor() as cursor:
        cursor.execute(update_query, (departamento, disciplina_id))

def delete_disciplina(disciplina_id):
    delete_query = "DELETE FROM Disciplinas WHERE codigo = %s"
    with get_cursor() as cursor:
        cursor.execute(delete_query, (disciplina_id,))