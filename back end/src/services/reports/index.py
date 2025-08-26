from src.services.avaluations.index import get_avaliacoes_by_ID
from src.db_connection.connection import get_cursor

def create_denuncia(id_estudante, id_avaliacao, motivo, avaliada=False):
    insert_query = '''
        INSERT INTO Denuncias (id_estudante, id_avaliacao, motivo, avaliada)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    '''
    with get_cursor() as cursor:
        cursor.execute(insert_query, (id_estudante, id_avaliacao, motivo, avaliada))
        denuncia_id = cursor.fetchone()[0]

    return {
        'id': denuncia_id,
        'id_estudante': id_estudante,
        'id_avaliacao': id_avaliacao,
        'motivo': motivo,
        'avaliada': avaliada
    }


def update_denuncia(denuncia_id, id_estudante=None, id_avaliacao=None, motivo=None, avaliada=None):
    update_values = []

    if id_estudante is not None:
        update_values.append(('id_estudante', id_estudante))
    if id_avaliacao is not None:
        update_values.append(('id_avaliacao', id_avaliacao))
    if motivo is not None:
        update_values.append(('motivo', motivo))
    if avaliada is not None:
        update_values.append(('avaliada', avaliada))

    set_clause = ', '.join([f'{field} = %s' for field, _ in update_values])

    update_query = f'''
        UPDATE Denuncias
        SET {set_clause}
        WHERE id = %s
    '''

    update_values.append(('denuncia_id', denuncia_id))
    update_values = [value for _, value in update_values]

    with get_cursor() as cursor:
        cursor.execute(update_query, update_values)

    return {
        'id': denuncia_id,
        'id_estudante': id_estudante,
        'id_avaliacao': id_avaliacao,
        'motivo': motivo,
        'avaliada': avaliada
    }


def get_all_denuncias():
    query = "SELECT * FROM Denuncias"
    with get_cursor() as cursor:
        cursor.execute(query)
        denuncias = cursor.fetchall()

    return [
        {
            'id': denuncia[0],
            'id_estudante': denuncia[1],
            'id_avaliacao': denuncia[2],
            'motivo': denuncia[3],
            'avaliada': denuncia[4]
        }
        for denuncia in denuncias
    ]


def get_denuncia_by_id(denuncia_id):
    query = "SELECT * FROM Denuncias WHERE id = %s"
    with get_cursor() as cursor:
        cursor.execute(query, (denuncia_id,))
        denuncia = cursor.fetchone()

    if denuncia is not None:
        return {
            'id': denuncia[0],
            'id_estudante': denuncia[1],
            'id_avaliacao': denuncia[2],
            'motivo': denuncia[3],
            'avaliada': denuncia[4]
        }
    else:
        return None


def get_denuncias_by_estudante_id(estudante_id):
    query = "SELECT * FROM Denuncias WHERE id_estudante = %s"
    with get_cursor() as cursor:
        cursor.execute(query, (estudante_id,))
        denuncias = cursor.fetchall()
    print(denuncias)

    return [
        {
            'id': denuncia[0],
            'id_estudante': denuncia[1],
            'id_avaliacao': denuncia[2],
            'motivo': denuncia[3],
            'avaliada': denuncia[4]
        }
        for denuncia in denuncias
    ]

def delete_denuncia(denuncia_id):
    query = "DELETE FROM Denuncias WHERE id = %s"
    with get_cursor() as cursor:
        cursor.execute(query, (denuncia_id,))
