-- Inserção de dados na tabela Estudantes
INSERT INTO Estudantes (nome, email, senha, matricula, curso)
VALUES ('João', 'joao@example.com', 'senha123', '202100001', 'Engenharia');

INSERT INTO Estudantes (nome, email, senha, matricula, curso)
VALUES ('Maria', 'maria@example.com', 'senha456', '202100002', 'Direito');

INSERT INTO Estudantes (nome, email, senha, matricula, curso)
VALUES ('Pedro', 'pedro@example.com', 'senha789', '202100003', 'Medicina');

-- Inserção de dados na tabela Comentarios
INSERT INTO Comentarios (texto, estudante_id, id_professor)
VALUES ('Ótimo professor!', 1, 1);

INSERT INTO Comentarios (texto, estudante_id, id_professor)
VALUES ('Precisa melhorar a didática.', 2, 1);

INSERT INTO Comentarios (texto, estudante_id, id_professor)
VALUES ('Excelente disciplina!', 3, 2);

-- Inserção de dados na tabela Disciplinas
INSERT INTO Disciplinas (nome, cod_depto)
VALUES ('Cálculo I', 1);

INSERT INTO Disciplinas (nome, cod_depto)
VALUES ('Introdução à Programação', 1);

INSERT INTO Disciplinas (nome, cod_depto)
VALUES ('Direito Civil', 2);
