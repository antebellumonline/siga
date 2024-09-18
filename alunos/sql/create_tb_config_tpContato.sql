CREATE TABLE tb_config_tpContato (
    id INT IDENTITY PRIMARY KEY,               -- Identificador único para o tipo de contato
    descricao NVARCHAR(255) NOT NULL UNIQUE,  -- Descrição do tipo de contato (ex: Celular Pessoal, E-mail Corporativo)
    inativo BIT NOT NULL DEFAULT 0            -- 0 = Ativo, 1 = Inativo
);
