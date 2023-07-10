from src.db_connection.connection import get_db_connection

def get_all_denuncias():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Denuncias"
    cursor.execute(query)

    denuncias = cursor.fetchall()

    cursor.close()
    conn.close()

    return denuncias


def get_denuncia_by_id(denuncia_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Denuncias WHERE id = %s"
    cursor.execute(query, (denuncia_id,))

    denuncia = cursor.fetchone()

    cursor.close()
    conn.close()

    return denuncia


def delete_denuncia(denuncia_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM Denuncias WHERE id = %s"
    cursor.execute(query, (denuncia_id,))

    conn.commit()

    cursor.close()
    conn.close()


def update_denuncia(denuncia_id, validada):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE Denuncias SET validada = %s WHERE id = %s"
    cursor.execute(query, (validada, denuncia_id))

    conn.commit()

    cursor.close()
    conn.close()
