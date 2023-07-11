from src.db_connection.connection import get_db_connection

def create_class(turma, periodo, professor, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto):
    conn = get_db_connection()
    cursor = conn.cursor()

    professor_id = get_professor_id_by_name(professor)
    departamento_id = get_departamento_id_by_name(cod_depto)

    insert_query = '''
        INSERT INTO Turmas (turma, periodo, professor_id, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    cursor.execute(insert_query, (turma, periodo, professor_id, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, departamento_id))
    class_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return {
        'class_id': class_id,
        'turma': turma,
        'periodo': periodo,
        'professor': professor,
        'horario': horario,
        'vagas_ocupadas': vagas_ocupadas,
        'total_vagas': total_vagas,
        'local': local,
        'cod_disciplina': cod_disciplina,
        'cod_depto': cod_depto
    }

def edit_class(class_id, turma=None, periodo=None, professor=None, horario=None, vagas_ocupadas=None, total_vagas=None, local=None, cod_disciplina=None, cod_depto=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    update_values = []

    if turma is not None:
        update_values.append(('turma', turma))
    if periodo is not None:
        update_values.append(('periodo', periodo))
    if professor is not None:
        professor_id = get_professor_id_by_name(professor)
        update_values.append(('professor_id', professor_id))
    if horario is not None:
        update_values.append(('horario', horario))
    if vagas_ocupadas is not None:
        update_values.append(('vagas_ocupadas', vagas_ocupadas))
    if total_vagas is not None:
        update_values.append(('total_vagas', total_vagas))
    if local is not None:
        update_values.append(('local', local))
    if cod_disciplina is not None:
        update_values.append(('cod_disciplina', cod_disciplina))
    if cod_depto is not None:
        departamento_id = get_departamento_id_by_name(cod_depto)
        update_values.append(('cod_depto', departamento_id))

    set_clause = ', '.join([f'{field} = %s' for field, _ in update_values])

    update_query = f'''
        UPDATE Turmas
        SET {set_clause}
        WHERE id = %s
    '''

    update_values.append(('class_id', class_id))
    update_values = [value for _, value in update_values]

    cursor.execute(update_query, update_values)
    conn.commit()

    cursor.close()
    conn.close()

    updated_class_data = get_class_by_id(class_id)  # Obter os dados atualizados da turma do banco de dados

    return updated_class_data


def get_professor_id_by_name(professor_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT id FROM Professores WHERE nome = %s
    '''
    cursor.execute(select_query, (professor_name,))
    professor_id = cursor.fetchone()

    cursor.close()
    conn.close()

    if professor_id:
        return professor_id[0]
    else:
        return None

def get_departamento_id_by_name(departamento_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT id FROM Departamentos WHERE nome = %s
    '''
    cursor.execute(select_query, (departamento_name,))
    departamento_id = cursor.fetchone()

    cursor.close()
    conn.close()

    if departamento_id:
        return departamento_id[0]
    else:
        return None


def get_classes():
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Turmas
    '''
    cursor.execute(select_query)
    classes = cursor.fetchall()

    cursor.close()
    conn.close()

    return classes

def get_class_by_id(class_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = '''
        SELECT * FROM Turmas WHERE id = %s
    '''
    cursor.execute(select_query, (class_id,))
    class_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return class_data

def delete_class(class_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    delete_query = '''
        DELETE FROM Turmas WHERE id = %s
    '''
    cursor.execute(delete_query, (class_id,))
    conn.commit()

    cursor.close()
    conn.close()