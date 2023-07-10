from db_connection.connection import get_db_connection

def create_disciplina(nome, departamento):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = "INSERT INTO Disciplinas (nome, departamento) VALUES (%s, %s)"
    cursor.execute(insert_query, (nome, departamento))
    conn.commit()
    cursor.close()
    conn.close()

# Service de leitura de disciplina por ID
def get_disciplina_by_id(disciplina_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = "SELECT * FROM Disciplinas WHERE id = %s"
    cursor.execute(select_query, (disciplina_id,))
    disciplina = cursor.fetchone()
    cursor.close()
    conn.close()
    return disciplina

# Service de leitura de todas as disciplinas
def get_all_disciplinas():
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = "SELECT * FROM Disciplinas"
    cursor.execute(select_query)
    disciplinas = cursor.fetchall()
    cursor.close()
    conn.close()
    return disciplinas

# Service de atualização de disciplina
def update_disciplina(disciplina_id, departamento):
    conn = get_db_connection()
    cursor = conn.cursor()
    update_query = "UPDATE Disciplinas SET departamento = %s WHERE id = %s"
    cursor.execute(update_query, (departamento, disciplina_id))
    conn.commit()
    cursor.close()
    conn.close()

# Service de exclusão de disciplina
def delete_disciplina(disciplina_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    delete_query = "DELETE FROM Disciplinas WHERE id = %s"
    cursor.execute(delete_query, (disciplina_id,))
    conn.commit()
    cursor.close()
    conn.close()