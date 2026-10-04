-- CONSULTAS DE VALIDAÇÃO NA TABELA raw_vendas

-- 1. Total de linhas e ids distintos (compare com o número de linhas do CSV original)
SELECT COUNT(*) AS total_linhas,
       COUNT(DISTINCT invoice_id) AS ids_distintos
FROM raw_vendas;

-- 2. Nulos nas colunas principais
SELECT
    COUNT(*) FILTER (WHERE invoice_id IS NULL) AS nulos_invoice_id,
    COUNT(*) FILTER (WHERE total IS NULL)      AS nulos_total,
    COUNT(*) FILTER (WHERE date IS NULL)       AS nulos_date,
    COUNT(*) FILTER (WHERE rating IS NULL)     AS nulos_rating
FROM raw_vendas;

-- 3. Valores das categorias (filial e cidade)
SELECT branch, city, COUNT(*) AS qtd
FROM raw_vendas
GROUP BY branch, city
ORDER BY branch;


-- CONSULTAS DE VALIDAÇÃO NA TABELA vendas_tratadas

-- 1. Total de linhas e ids distintos
SELECT COUNT(*) AS total_linhas,
       COUNT(DISTINCT id_venda) AS ids_distintos
FROM vendas_tratadas;

-- 2. Soma do valor total na raw x tratada e datas/horas que falharam na conversão
SELECT
    (SELECT ROUND(SUM(CAST(total AS NUMERIC)), 2) FROM raw_vendas)  AS soma_raw,
    (SELECT ROUND(SUM(valor_total), 2) FROM vendas_tratadas)        AS soma_tratada,
    (SELECT COUNT(*) FROM vendas_tratadas
     WHERE data_venda IS NULL OR hora_venda IS NULL)                AS datas_horas_nulas;