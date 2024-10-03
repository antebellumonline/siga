CREATE TABLE tb_centroProva-exames (
    id INT IDENTITY PRIMARY KEY,                -- Identificador único para cada Exame realizado
    certificacao INT NOT NULL,                -- Referência à tabela tb_certificacao
    centroProva INT NOT NULL,                 -- Referência à tabela tb_centroProva
    aluno INT NOT NULL,                       -- Referência à tabela tb_aluno
    data DATETIME NOT NULL,                      -- Data e hora do exame
    presenca BIT NOT NULL DEFAULT 0,            -- 0 = Ausente, 1 = Presente
    cancelado BIT NOT NULL DEFAULT 0,           -- 0 = Não cancelado, 1 = Cancelado
    inativo BIT NOT NULL DEFAULT 0,             -- 0 = Ativo, 1 = Inativo
    FOREIGN KEY (certificacao) REFERENCES tb_certificacao(id) ON DELETE CASCADE,  -- Chave estrangeira
    FOREIGN KEY (centroProva) REFERENCES tb_centroProva(id) ON DELETE CASCADE,    -- Chave estrangeira
    FOREIGN KEY (aluno) REFERENCES tb_aluno(uid) ON DELETE CASCADE                -- Chave estrangeira
);