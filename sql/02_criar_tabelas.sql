
-- Criação da Tabela Raw: dados brutos do CSV original (sem tratamento/validação) 

CREATE TABLE raw_vendas (
    id_raw SERIAL PRIMARY KEY,
    invoice_id VARCHAR(50),
    branch VARCHAR(10),
    city VARCHAR(100),
    customer_type VARCHAR(50),
    gender VARCHAR(20),
    product_line VARCHAR(150),
    unit_price VARCHAR(50),
    quantity VARCHAR(50),
    tax_5 VARCHAR(50),
    total VARCHAR(50),
    date VARCHAR(50),
    time VARCHAR(50),
    payment VARCHAR(50),
    cogs VARCHAR(50),
    gross_margin_percentage VARCHAR(50),
    gross_income VARCHAR(50),
    rating VARCHAR(50)
);

-- Criação da Tabela Tratada: onde serão inseridos os dados limpos e validados

DROP TABLE IF EXISTS vendas_tratadas;

CREATE TABLE vendas_tratadas (
    id_venda VARCHAR(50) PRIMARY KEY,
    filial VARCHAR(10) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    tipo_cliente VARCHAR(50),
    genero VARCHAR(20),
    linha_produto VARCHAR(150) NOT NULL,
    preco_unitario NUMERIC(10,2) CHECK (preco_unitario >= 0),
    quantidade INTEGER CHECK (quantidade > 0),
    imposto NUMERIC(10,2) CHECK (imposto >= 0),
    valor_total NUMERIC(12,2) CHECK (valor_total >= 0),
    data_venda DATE,
    hora_venda TIME,
    forma_pagamento VARCHAR(50) NOT NULL,
    custo_mercadoria NUMERIC(12,2) CHECK (custo_mercadoria >= 0),
    margem_percentual NUMERIC(10,2),
    receita_bruta NUMERIC(12,2) CHECK (receita_bruta >= 0),
    avaliacao NUMERIC(4,2) CHECK (avaliacao >= 0 AND avaliacao <= 10),
    dia_semana VARCHAR(20),
    nome_mes VARCHAR(20)
);