CREATE TABLE tb_aluno (
    UID INT IDENTITY(10000000,1) PRIMARY KEY, -- Código único, iniciando em 10000000
    nome NVARCHAR(255) NOT NULL,             -- Nome completo do aluno
    cpf CHAR(11) NOT NULL,                   -- CPF do aluno (sem formatação)
    cep CHAR(8),                             -- CEP (somente números, sem formatação)
    endereco NVARCHAR(255),                  -- Endereço
    numero NVARCHAR(10),                     -- Número
    complemento NVARCHAR(255),               -- Complemento
    bairro NVARCHAR(255),                    -- Bairro
    cidade INT,                              -- Código da cidade conforme IBGE
    observacao NVARCHAR(MAX),                -- Observações adicionais
    inativo BIT NOT NULL DEFAULT 0           -- 0 = Ativo, 1 = Inativo
);
