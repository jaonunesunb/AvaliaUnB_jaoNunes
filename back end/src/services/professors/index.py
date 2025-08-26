import math
from src.db_connection.connection import get_cursor
from flask import request


def create_professor(nome, departamento):
    select_departamento_query = "SELECT id FROM Departamentos WHERE id = %s"
    with get_cursor() as cursor:
        cursor.execute(select_departamento_query, (departamento,))
        departamento_exists = cursor.fetchone()

        if not departamento_exists:
            return None

        insert_query = "INSERT INTO Professores (nome, departamento_id) VALUES (%s, %s) RETURNING id, nome, departamento_id"
        cursor.execute(insert_query, (nome, departamento))
        professor = cursor.fetchone()

    return professor

def get_professor_by_id(professor_id):
    select_query = "SELECT * FROM Professores WHERE id = %s"
    with get_cursor() as cursor:
        cursor.execute(select_query, (professor_id,))
        professor = cursor.fetchone()
    return professor

def get_all_professores(page, per_page):
    select_query = "SELECT * FROM Professores ORDER BY id OFFSET %s LIMIT %s"
    offset = (page - 1) * per_page
    limit = min(per_page, 50)
    with get_cursor() as cursor:
        cursor.execute(select_query, (offset, limit))
        column_names = [desc[0] for desc in cursor.description]
        professores = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    total_professores = 50
    total_pages = math.ceil(total_professores / per_page)
    current_page = page
    previous_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None
    pages = list(range(1, total_pages + 1))

    return {
        'professores': professores,
        'total_pages': total_pages,
        'current_page': current_page,
        'previous_page': previous_page,
        'next_page': next_page,
        'pages': pages
    }
    
def update_professor(professor_id, nome=None, departamento=None):
    with get_cursor() as cursor:
        if departamento is not None:
            select_departamento_query = "SELECT id FROM Departamentos WHERE id = %s"
            cursor.execute(select_departamento_query, (departamento,))
            departamento_exists = cursor.fetchone()
            if not departamento_exists:
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

        select_query = "SELECT * FROM Professores WHERE id = %s"
        cursor.execute(select_query, (professor_id,))
        updated_professor = cursor.fetchone()

    return updated_professor


def delete_professor(professor_id):
    delete_query = "DELETE FROM Professores WHERE id = %s"
    with get_cursor() as cursor:
        cursor.execute(delete_query, (professor_id,))
