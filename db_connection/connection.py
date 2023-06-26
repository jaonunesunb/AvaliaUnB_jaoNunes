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

    create_estudantes_table_query = '''
        CREATE TABLE IF NOT EXISTS Estudantes (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
            senha TEXT NOT NULL
            matricula TEXT NOT NULL
            curso TEXT 
        );
    '''
    cursor.execute(create_estudantes_table_query)

    create_professores_table_query = '''
        CREATE TABLE IF NOT EXISTS Professores (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            departamento TEXT NOT NULL
        );
    '''
    cursor.execute(create_professores_table_query)

    create_comentarios_table_query = '''
        CREATE TABLE IF NOT EXISTS Comentarios (
            id SERIAL PRIMARY KEY,
            texto TEXT NOT NULL,
            estudante_id INTEGER REFERENCES Estudantes (id),
            id_professor INTEGER REFERENCES Professores (id)
        );
    '''
    cursor.execute(create_comentarios_table_query)

    create_disciplinas_table_query = '''
        CREATE TABLE IF NOT EXISTS Disciplinas (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            departamento TEXT
        );
    '''
    cursor.execute(create_disciplinas_table_query)

 
    create_turmas_table_query = '''
        CREATE TABLE IF NOT EXISTS Turmas (
            id SERIAL PRIMARY KEY,
            id_disciplina INTEGER REFERENCES Disciplinas (id),
            id_professor INTEGER REFERENCES Professores (id),
            semestre TEXT
        );
    '''
    cursor.execute(create_turmas_table_query)

    create_denuncias_table_query = '''
        CREATE TABLE IF NOT EXISTS Denuncias (
            id SERIAL PRIMARY KEY,
            id_estudante INTEGER REFERENCES Estudantes (id),
            id_comentario INTEGER REFERENCES Comentarios (id),
            motivo TEXT
        );
    '''
    cursor.execute(create_denuncias_table_query)

    conn.commit()

    cursor.close()
    conn.close()