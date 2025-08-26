from src.services.disciplines.index import get_disciplina_by_id
from src.services.professors.index import get_professor_by_id
from src.db_connection.connection import get_cursor

def create_class(turma, periodo, professor, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto):
    professor_id = get_professor_id_by_name(professor)
    departamento_id = get_departamento_id_by_name(cod_depto)

    insert_query = '''
        INSERT INTO Turmas (turma, periodo, professor_id, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    with get_cursor() as cursor:
        cursor.execute(insert_query, (turma, periodo, professor_id, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, departamento_id))
        class_id = cursor.fetchone()[0]

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

    with get_cursor() as cursor:
        cursor.execute(update_query, update_values)

    updated_class_data = get_class_by_id(class_id)

    return updated_class_data


def get_professor_id_by_name(professor_name):
    select_query = '''
        SELECT id FROM Professores WHERE nome = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (professor_name,))
        professor_id = cursor.fetchone()

    if professor_id:
        return professor_id[0]
    else:
        return None

def get_departamento_id_by_name(departamento_name):
    select_query = '''
        SELECT id FROM Departamentos WHERE nome = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (departamento_name,))
        departamento_id = cursor.fetchone()

    if departamento_id:
        return departamento_id[0]
    else:
        return None


def get_classes(page, per_page):
    select_query = '''
        SELECT * FROM Turmas
        ORDER BY id
        OFFSET %s LIMIT %s
    '''
    offset = (page - 1) * per_page
    with get_cursor() as cursor:
        cursor.execute(select_query, (offset, per_page))
        classes = cursor.fetchall()

    return classes


def get_class_by_id(class_id):
    select_query = '''
        SELECT * FROM Turmas WHERE id = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(select_query, (class_id,))
        class_data = cursor.fetchone()

    if class_data:
        return {
            'id': class_data[0],
            'turma': class_data[1],
            'periodo': class_data[2],
            'disciplina': get_disciplina_by_id(class_data[8])[1],
            'professor': get_professor_by_id(class_data[3])[1],
            'horario': class_data[4],
            'vagas_ocupadas': class_data[5],
            'total_vagas': class_data[6],
            'local': class_data[7],
            'cod_disciplina': class_data[8],
            'cod_depto': class_data[9]
        }
    else:
        return None
    
def delete_class(class_id):
    delete_query = '''
        DELETE FROM Turmas WHERE id = %s
    '''
    with get_cursor() as cursor:
        cursor.execute(delete_query, (class_id,))
