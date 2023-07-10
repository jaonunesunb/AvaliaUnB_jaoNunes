CREATE TABLE IF NOT EXISTS Departamentos (
    id INTEGER PRIMARY KEY,
    nome TEXT
);

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

CREATE TABLE IF NOT EXISTS Professores (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    departamento_id INTEGER REFERENCES Departamentos (id)
);

CREATE TABLE IF NOT EXISTS Disciplinas (
    codigo TEXT PRIMARY KEY,
    nome TEXT,
    departamento_id INTEGER REFERENCES Departamentos (id)
);

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

CREATE TABLE IF NOT EXISTS Avaliacoes (
    id SERIAL PRIMARY KEY,
    id_estudante INTEGER REFERENCES Estudantes (id),
    id_turma INTEGER REFERENCES Turmas (id),
    nota INTEGER,
    comentario TEXT
);

CREATE TABLE IF NOT EXISTS Denuncias (
    id SERIAL PRIMARY KEY,
    id_estudante INTEGER REFERENCES Estudantes (id),
    id_avaliacao INTEGER REFERENCES Avaliacoes (id),
    motivo TEXT,
    avaliada BOOLEAN DEFAULT FALSE
);
