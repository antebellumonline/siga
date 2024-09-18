CREATE TABLE tb_aluno_contato (
    id INT IDENTITY PRIMARY KEY,                -- Identificador único para o contato
    uidAluno INT NOT NULL,                     -- Código que relaciona com a tabela tb_aluno
    codTpContato INT NOT NULL,                 -- Código que relaciona com a tabela tb_config_tpContato
    contato NVARCHAR(255) NOT NULL,            -- Dados de contato (celular, telefone ou e-mail)
    detalhe NVARCHAR(MAX),                     -- Observações adicionais
    FOREIGN KEY (uidAluno) REFERENCES tb_aluno(UID), -- Relacionamento com a tabela tb_aluno
    FOREIGN KEY (codTpContato) REFERENCES tb_config_tpContato(id) -- Relacionamento com a tabela tb_config_tpContato
);
