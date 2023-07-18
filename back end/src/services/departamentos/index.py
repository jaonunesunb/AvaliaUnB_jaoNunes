from src.db_connection.connection import get_db_connection

def create_departamento(nome):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO Departamentos (nome)
        VALUES (%s)
        RETURNING id
    '''
    cursor.execute(insert_query, (nome,))
    departamento_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return {
        'departamento_id': departamento_id,
        'nome': nome
    }

def get_departamentos():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT id, nome FROM Departamentos
    '''
    cursor.execute(select_query)
    departamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    departamentos_list = [{'departamento_id': departamento[0], 'nome': departamento[1]} for departamento in departamentos]
    return departamentos_list

def get_departamento_by_id(departamento_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT id, nome FROM Departamentos WHERE id = %s
    '''
    cursor.execute(select_query, (departamento_id,))
    departamento = cursor.fetchone()

    cursor.close()
    conn.close()

    if departamento:
        departamento_data = {'departamento_id': departamento[0], 'nome': departamento[1]}
        return departamento_data
    else:
        return None

def get_departamento_name(departamento_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT nome FROM Departamentos WHERE id = %s
    '''
    cursor.execute(select_query, (departamento_id,))
    departamento = cursor.fetchone()

    cursor.close()
    conn.close()

    if departamento:
        return departamento[0]
    else:
        return None




