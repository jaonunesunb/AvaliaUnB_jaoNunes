import csv
from src.db_connection.connection import get_db_connection
from src.services.students.index import convert_image_to_base64

def insert_departments():
    conn = get_db_connection()
    cursor = conn.cursor()

    with open('src/CSVs/departamentos_2022-1.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Pula o cabeçalho do CSV

        for row in csv_data:
            department_id = int(row[0])
            department_name = row[1]

            insert_query = '''
                INSERT INTO Departamentos (id, nome)
                VALUES (%s, %s)
            '''
            cursor.execute(insert_query, (department_id, department_name))

    conn.commit()
    cursor.close()
    conn.close()

def insert_disciplines():
    conn = get_db_connection()
    cursor = conn.cursor()

    with open('src/CSVs/disciplinas_2022-1.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Pula o cabeçalho do CSV

        for row in csv_data:
            discipline_code = row[0]
            discipline_name = row[1]
            department_id = int(row[2])

            # Verifica se o código de disciplina já existe na tabela
            select_query = '''
                SELECT codigo FROM Disciplinas WHERE codigo = %s
            '''
            cursor.execute(select_query, (discipline_code,))
            existing_code = cursor.fetchone()

            if existing_code:
                # Código de disciplina já existe, faça o tratamento adequado
                print(f'O código de disciplina {discipline_code} já existe.')
            else:
                # Código de disciplina não existe, faça a inserção
                insert_query = '''
                    INSERT INTO Disciplinas (codigo, nome, departamento_id)
                    VALUES (%s, %s, %s)
                '''
                cursor.execute(insert_query, (discipline_code, discipline_name, department_id))

    conn.commit()
    cursor.close()
    conn.close()

def insert_classes():
    conn = get_db_connection()
    cursor = conn.cursor()

    with open('src/CSVs/turmas_2022-1.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Pula o cabeçalho do CSV

        for row in csv_data:
            class_name = row[0]
            period = row[1]
            professor = row[2]
            schedule = row[3]
            occupied_seats = int(row[4])
            total_seats = int(row[5]) if row[5] else 0  # Verifica se o campo não está vazio
            location = row[6]
            discipline_id = row[7]
            department_id = int(row[8])

            insert_query = '''
                INSERT INTO Turmas (turma, periodo, professor, horario, vagas_ocupadas, total_vagas, local, cod_disciplina, cod_depto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (class_name, period, professor, schedule, occupied_seats, total_seats, location, discipline_id, department_id))

    conn.commit()
    cursor.close()
    conn.close()

def insert_students():
    conn = get_db_connection()
    cursor = conn.cursor()

    students_data = [
        ('João', 'joao@example.com', 'senha123', '202100001', 'Biblioteconomia', 'src/assets/joao_photo.jpg', False),
        ('Maria', 'maria@example.com', 'senha456', '202100002', 'Direito', 'src/assets/maria_photo.jpg', False),
        ('Pedro', 'pedro@example.com', 'senha789', '202100003', 'Medicina', 'src/assets/pedro_photo.jpg', True)
    ]

    for student in students_data:
        nome, email, senha, matricula, curso, foto_path, is_adm = student

        # Converte a imagem para base64
        foto_base64 = convert_image_to_base64(foto_path)

        insert_query = '''
            INSERT INTO Estudantes (nome, email, senha, matricula, curso, foto, is_adm)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (nome, email, senha, matricula, curso, foto_base64, is_adm))

    conn.commit()
    cursor.close()
    conn.close()
    
def insert_professors():
    conn = get_db_connection()
    cursor = conn.cursor()


    # Inserção de professores
    professors_data = [
        ('Joana Pereira da Silva', 473),
        ('Carlos Silvio Santos', 674),
        ('Mariana Santos da Silva', 518)
    ]

    for professor in professors_data:
        insert_query = '''
            INSERT INTO Professores (nome, departamento_id)
            VALUES (%s, %s)
        '''
        cursor.execute(insert_query, professor)

    conn.commit()
    cursor.close()
    conn.close()

def insert_evaluations():
    conn = get_db_connection()
    cursor = conn.cursor()

    evaluations_data = [
        (1, 422, 8, 'Ótimo professor!'),
        (1, 113, 7, 'Aulas bem estruturadas.'),
        (2, 185, 6, 'Professor com dificuldades em explicar.'),
        (1, 122, 1, 'Comportamento inadequado do professor'),
        (2, 193, 1, 'Turma com conteúdo desorganizado.'),
        (3, 301, 3, 'Professor não comparece às aulas.')
    ]

    for evaluation in evaluations_data:
        id_estudante, id_turma, nota, comentario = evaluation

        insert_query = '''
            INSERT INTO Avaliacoes (id_estudante, id_turma, nota, comentario)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (id_estudante, id_turma, nota, comentario))

    conn.commit()
    cursor.close()
    conn.close()

def insert_reports():
    conn = get_db_connection()
    cursor = conn.cursor()

    reports_data = [
        (1, 4, 'O professor tinha o comportamento adequado.', True),
        (2, 5, 'A falta de organzação veio da secretaria do curso.', False),
        (3, 6, 'O professor avisou que as aulas seriam online.', False)
    ]

    for report in reports_data:
        id_estudante, id_avaliacao, motivo, avaliada = report

        insert_query = '''
            INSERT INTO Denuncias (id_estudante, id_avaliacao, motivo, avaliada)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (id_estudante, id_avaliacao, motivo, avaliada))

    conn.commit()
    cursor.close()
    conn.close()


# Chamada das funções para inserção dos dados
insert_departments()
insert_disciplines()
insert_classes()
insert_students()
insert_professors()
insert_evaluations()
insert_reports()