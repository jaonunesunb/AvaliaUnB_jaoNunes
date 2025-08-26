from src.db_connection.connection import get_cursor

def create_departamento(nome):
    insert_query = '''
        INSERT INTO Departamentos (nome)
        VALUES (%s)
        RETURNING id
    '''
    with get_cursor() as cursor:
        cursor.execute(insert_query, (nome,))
        departamento_id = cursor.fetchone()[0]

    return {
        'departamento_id': departamento_id,
        'nome': nome
    }

def get_departamentos():
    select_query = '''
        SELECT id, nome FROM Departamentos
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query)
        departamentos = cursor.fetchall()

    departamentos_list = [{'departamento_id': departamento[0], 'nome': departamento[1]} for departamento in departamentos]
    return departamentos_list

def get_departamento_by_id(departamento_id):
    select_query = '''
        SELECT id, nome FROM Departamentos WHERE id = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (departamento_id,))
        departamento = cursor.fetchone()

    if departamento:
        departamento_data = {'departamento_id': departamento[0], 'nome': departamento[1]}
        return departamento_data
    else:
        return None

def get_departamento_name(departamento_id):
    select_query = '''
        SELECT nome FROM Departamentos WHERE id = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (departamento_id,))
        departamento = cursor.fetchone()

    if departamento:
        return departamento[0]
    else:
        return None
