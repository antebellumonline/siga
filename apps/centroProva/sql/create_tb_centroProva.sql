CREATE TABLE tb_centroProva (
    id INT IDENTITY PRIMARY KEY,                -- Identificador único para o Centro de Provas
    nome VARCHAR(255) NOT NULL,                 -- Nome do Centro de Provas
    inativo BOOLEAN DEFAULT FALSE               -- 0 = Ativo, 1 = Inativo
);