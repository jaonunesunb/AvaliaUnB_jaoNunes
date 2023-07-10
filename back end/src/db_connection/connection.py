import psycopg2
from dotenv import dotenv_values

def get_db_connection():
    # Carrega as variáveis de ambiente do arquivo .env
    env_variables = dotenv_values()

    # Obtém as configurações do banco de dados do arquivo .env
    db_config = {
        'dbname': env_variables['DB_NAME'],
        'user': env_variables['DB_USER'],
        'password': env_variables['DB_PASSWORD'],
        'host': env_variables['DB_HOST'],
        'port': env_variables['DB_PORT']
    }

    # Cria a conexão com o banco de dados usando psycopg2
    conn = psycopg2.connect(
        dbname=db_config['dbname'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_departamentos_table_query = '''
        CREATE TABLE IF NOT EXISTS Departamentos (
            id INTEGER PRIMARY KEY,
            nome TEXT
        );
    '''
    cursor.execute(create_departamentos_table_query)

    create_estudantes_table_query = '''
        CREATE TABLE IF NOT EXISTS Estudantes (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            matricula TEXT NOT NULL,
            is_adm BOOLEAN DEFAULT FALSE,
            curso TEXT,
            foto BYTEA
        );
    '''
    cursor.execute(create_estudantes_table_query)

    create_professores_table_query = '''
        CREATE TABLE IF NOT EXISTS Professores (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            departamento_id INTEGER REFERENCES Departamentos (id)
        );
    '''
    cursor.execute(create_professores_table_query)

    create_disciplinas_table_query = '''
        CREATE TABLE IF NOT EXISTS Disciplinas (
            codigo TEXT PRIMARY KEY,
            nome TEXT,
            departamento_id INTEGER REFERENCES Departamentos (id)
        );
    '''
    cursor.execute(create_disciplinas_table_query)

    create_turmas_table_query = '''
        CREATE TABLE IF NOT EXISTS Turmas (
            id SERIAL PRIMARY KEY,
            turma TEXT NOT NULL,
            periodo TEXT NOT NULL,
            professor TEXT NOT NULL,
            horario TEXT NOT NULL,
            vagas_ocupadas INTEGER NOT NULL,
            total_vagas INTEGER NOT NULL,
            local TEXT NOT NULL,
            cod_disciplina TEXT REFERENCES Disciplinas (codigo),
            cod_depto INTEGER REFERENCES Departamentos (id)
        );
    '''
    cursor.execute(create_turmas_table_query)

    create_avaliacoes_table_query = '''
        CREATE TABLE IF NOT EXISTS Avaliacoes (
            id SERIAL PRIMARY KEY,
            id_estudante INTEGER REFERENCES Estudantes (id),
            id_turma INTEGER REFERENCES Turmas (id),
            nota INTEGER,
            comentario TEXT
        );
    '''
    cursor.execute(create_avaliacoes_table_query)

    create_denuncias_table_query = '''
        CREATE TABLE IF NOT EXISTS Denuncias (
            id SERIAL PRIMARY KEY,
            id_estudante INTEGER REFERENCES Estudantes (id),
            id_avaliacao INTEGER REFERENCES Avaliacoes (id),
            motivo TEXT,
            avaliada BOOLEAN DEFAULT FALSE
        );
    '''
    cursor.execute(create_denuncias_table_query)

    conn.commit()

    cursor.close()
    conn.close()
