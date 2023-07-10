CREATE VIEW DisciplinasRanking AS
SELECT d.codigo, d.nome, AVG(a.nota) AS media_nota
FROM Disciplinas d
INNER JOIN Turmas t ON t.cod_disciplina = d.codigo
INNER JOIN Avaliacoes a ON a.id_turma = t.id
GROUP BY d.codigo, d.nome
ORDER BY media_nota DESC;
