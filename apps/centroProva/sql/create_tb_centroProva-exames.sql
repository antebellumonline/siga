CREATE TABLE tb_centroProva_exames (
    id INT IDENTITY PRIMARY KEY,                -- Identificador único para cada Exame realizado
    certificacao INT NOT NULL,                  -- Referência à tabela tb_certificacao
    centroProva INT NOT NULL,                   -- Referência à tabela tb_centroProva
    aluno INT NOT NULL,                         -- Referência à tabela tb_aluno
    data DATETIME NOT NULL,                     -- Data e hora do exame
    presenca BIT NOT NULL DEFAULT 0,            -- 0 = Ausente, 1 = Presente
    cancelado BIT NOT NULL DEFAULT 0,           -- 0 = Não cancelado, 1 = Cancelado
    inativo BIT NOT NULL DEFAULT 0,             -- 0 = Ativo, 1 = Inativo
    observacao TEXT NULL,                       -- Campo para observações, opcional
    FOREIGN KEY (certificacao) REFERENCES tb_certificacao(id) ON DELETE NO ACTION,  -- Chave estrangeira
    FOREIGN KEY (centroProva) REFERENCES tb_centroProva(id) ON DELETE NO ACTION,    -- Chave estrangeira
    FOREIGN KEY (aluno) REFERENCES tb_aluno(uid) ON DELETE NO ACTION,                -- Chave estrangeira
    CONSTRAINT unique_aluno_data UNIQUE (aluno, data)  -- Restrição única para evitar exames simultâneos do mesmo aluno
);
