-- -----------------------------------------------------
-- Nome: Guilherme Mateus Alves, Rodrigo da Silva
-- -----------------------------------------------------


-- -----------------------------------------------------
-- Estabelecimentos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS estabelecimentos (
  id_estabelecimento SERIAL PRIMARY KEY,
  telefone VARCHAR(15) NOT NULL,
  cnpj VARCHAR(18) NOT NULL,
  UNIQUE(cnpj)
);
-- -----------------------------------------------------
-- Funcionarios
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS funcionarios (
  id_funcionario SERIAL,
  nome VARCHAR(50) NOT NULL,
  cpf VARCHAR(14) UNIQUE NOT NULL,
  id_estabelecimento INT  NOT NULL,
  PRIMARY KEY (id_funcionario),
  CONSTRAINT fk_funcionarios_estabelecimentos FOREIGN KEY (id_estabelecimento) REFERENCES estabelecimentos (id_estabelecimento) ON DELETE CASCADE,
  UNIQUE(cpf)
);

-- -----------------------------------------------------
-- Fornecedores
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS fornecedores (
  id_fornecedor SERIAL,
  nome VARCHAR(50) NOT NULL,
  cnpj VARCHAR(18) NOT NULL,
  telefone VARCHAR(15) NOT NULL,
  email VARCHAR(100) NULL,
  PRIMARY KEY (id_fornecedor),
  UNIQUE (cnpj)
);
-- -----------------------------------------------------
-- Produtos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS produtos (
  id_produto SERIAL,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100) NULL,
  PRIMARY KEY (id_produto));
-- -----------------------------------------------------
-- Pedidos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedidos (
  id_pedido SERIAL,
  data_pedido TIMESTAMP NOT NULL,
  id_estabelecimento INT  NOT NULL,
  id_funcionario INT  NOT NULL,
  id_fornecedor INT  NOT NULL,
  PRIMARY KEY (id_pedido),
  CONSTRAINT fk_pedidos_estabelecimento FOREIGN KEY (id_estabelecimento) REFERENCES estabelecimentos (id_estabelecimento) ON DELETE CASCADE ,
  CONSTRAINT fk_pedidos_funcionarios FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario) ON DELETE CASCADE ,
  CONSTRAINT fk_pedidos_fornecedores FOREIGN KEY (id_fornecedor) REFERENCES fornecedores (id_fornecedor) ON DELETE CASCADE 
);

-- -----------------------------------------------------
-- Vendas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS vendas (
  id_venda SERIAL,
  data_venda TIMESTAMP NOT NULL,
  id_estabelecimento INT  NOT NULL,
  id_funcionario INT  NOT NULL,
  PRIMARY KEY (id_venda),
  CONSTRAINT fk_vendas_estabelecimentos FOREIGN KEY (id_estabelecimento) REFERENCES estabelecimentos (id_estabelecimento) ON DELETE CASCADE ,
  CONSTRAINT fk_vendas_funcionarios FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario) ON DELETE CASCADE 
);

-- -----------------------------------------------------
-- Pedidos_produtos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedidos_produtos (
  id_pedido_produto SERIAL,
  quantidade INT NOT NULL,
  valor_unitario DECIMAL(7, 2) NOT NULL,
  id_produto INT  NOT NULL,
  id_pedido INT NOT NULL,
  PRIMARY KEY (id_pedido_produto, id_produto, id_pedido),
  CONSTRAINT fk_pedidos_produtos FOREIGN KEY (id_produto) REFERENCES produtos (id_produto) ON DELETE CASCADE ,
  CONSTRAINT fk_pedidos_pedidos FOREIGN KEY (id_pedido) REFERENCES pedidos (id_pedido) ON DELETE CASCADE 
);

-- -----------------------------------------------------
-- Vendas_produtos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS vendas_produtos (
  id_venda_produto SERIAL,
  quantidade INT NOT NULL,
  valor_unitario DECIMAL(7, 2) NOT NULL,
  id_venda INT NOT NULL,
  id_produto INT  NOT NULL,
  PRIMARY KEY (id_venda_produto, id_venda, id_produto),
  CONSTRAINT fk_vendas_produtos_venda FOREIGN KEY (id_venda) REFERENCES vendas (id_venda) ON DELETE CASCADE ,
  CONSTRAINT fk_vendas_produtos_produtos FOREIGN KEY (id_produto) REFERENCES produtos (id_produto) ON DELETE CASCADE 
);
-- -----------------------------------------------------
-- Estabelecimentos_produtos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS estabelecimentos_produtos (
  id_estabelecimento SERIAL,
  id_produto INT  NOT NULL,
  quantidade INT NOT NULL,
  PRIMARY KEY (id_estabelecimento, id_produto),
  CONSTRAINT fk_estabelecimentos_produtos_estabelecimentos FOREIGN KEY (id_estabelecimento) REFERENCES estabelecimentos (id_estabelecimento) ON DELETE CASCADE ,
  CONSTRAINT fk_estabelecimentos_produtos_produtos FOREIGN KEY (id_produto) REFERENCES produtos (id_produto) ON DELETE CASCADE 
);

-- -----------------------------------------------------
-- Estabelecimentos (insert)
-- -----------------------------------------------------
INSERT INTO
  estabelecimentos (telefone, cnpj)
VALUES
  ('11987654321', '85957777000100'),
  ('21987654321', '65079212000151'),
  ('31987654321', '60493130000135'),
  ('61987654321', '13549096000193'),
  ('71987654321', '76663246000105'),
  ('41987654321', '37109029000116'),
  ('85987654321', '16711426000193'),
  ('81987654321', '96199447000100'),
  ('51987654321', '79368162000137'),
  ('92987654321', '93386485000184');
  commit;
-- -----------------------------------------------------
-- Funcionarios (insert)
-- -----------------------------------------------------
INSERT INTO funcionarios (nome, cpf, id_estabelecimento)
VALUES
  ('João Silva', '12345678900',1),
  ('Pedro Santos', '23456789001',2),
  ('Maria Oliveira', '34567890102',3),
  ('José Rodrigues', '45678901203',4),
  ('Paulo Souza', '56789012304',5),
  ('Ana Pereira', '67890123405',6),
  ('Marcio Almeida', '78901234506',7),
  ('Lucas Lima', '89012345607',8),
  ('Juliana Silva', '90123456708',9),
  ('Luiz Santos', '01234567890',10),
  ('Matheus Santos', '12345748900', 1),
  ('Guilherme Oliveira', '23456956001', 2),
  ('Neymar Silva', '34567812345', 3),
  ('Jorge Matheus', '45671234503', 4),
  ('José Felipe', '512345012304', 5),
  ('Virginia Ferrari', '65432123405', 6),
  ('Valeria Almeida', '78123454506', 7),
  ('Gustavo Lima', '89012309876', 8),
  ('Juliana Soares', '90123467890', 9),
  ('Silvio Santos', '01234549280', 10);
  commit;
-- -----------------------------------------------------
-- Fornecedores (insert)
-- -----------------------------------------------------
INSERT INTO
  fornecedores (nome, cnpj, telefone, email)
VALUES
  (
    'Fornecedor A',
    '12345678901230',
    '11999999999',
    'fornecedor_a@exemplo.com'
  ),
  (
    'Fornecedor B',
    '12345678901235',
    '11999999998',
    'fornecedor_b@exemplo.com'
  ),
  (
    'Fornecedor C',
    '12345678901236',
    '11999999997',
    'fornecedor_c@exemplo.com'
  ),
  (
    'Fornecedor D',
    '12345678901237',
    '11999999996',
    'fornecedor_d@exemplo.com'
  ),
  (
    'Fornecedor E',
    '12345678901238',
    '11999999995',
    'fornecedor_e@exemplo.com'
  ),
  (
    'Fornecedor F',
    '12345678901239',
    '11999999994',
    'fornecedor_f@exemplo.com'
  ),
  (
    'Fornecedor G',
    '12345678901240',
    '11999999993',
    'fornecedor_g@exemplo.com'
  ),
  (
    'Fornecedor H',
    '12345678901241',
    '11999999992',
    'fornecedor_h@exemplo.com'
  ),
  (
    'Fornecedor I',
    '12345678901242',
    '11999999991',
    'fornecedor_i@exemplo.com'
  ),
  (
    'Fornecedor J',
    '12345678901243',
    '11999999990',
    'fornecedor_j@exemplo.com'
  );
commit;
-- -----------------------------------------------------
-- Produtos (insert)
-- -----------------------------------------------------
INSERT INTO
  produtos (nome)
VALUES
  ('Cerveja OPA Bier Lata'),
  ('Refrigerante Coca Cola 2l'),
  ('Carne bovina 1kg'),
  ('Maçã Und.'),
  ('Alface Und.'),
  ('Cenoura Und.'),
  ('Queijo Tirol 400g'),
  ('Bolo de Cenoura Und.'),
  ('Coxinha Und.'),
  ('Macarrão Renata C/ Ovos 500g');
commit;
-- -----------------------------------------------------
-- Pedidos (insert)
-- -----------------------------------------------------
INSERT INTO
  pedidos (
    data_pedido,
    id_estabelecimento,
    id_funcionario,
    id_fornecedor
  )
VALUES
  ('2022-01-01 10:00:00', 1, 1, 1),
  ('2022-01-02 11:00:00', 2, 2, 2),
  ('2022-01-03 12:00:00', 3, 3, 3),
  ('2022-01-04 13:00:00', 4, 4, 4),
  ('2022-01-05 14:00:00', 5, 5, 5),
  ('2022-01-06 15:00:00', 6, 6, 6),
  ('2022-01-07 16:00:00', 7, 7, 7),
  ('2022-01-08 17:00:00', 8, 8, 8),
  ('2022-01-09 18:00:00', 9, 9, 9),
  ('2022-01-10 19:00:00', 10, 10, 10);
commit;
-- -----------------------------------------------------
-- Pedidos_produtos (insert)
-- -----------------------------------------------------
INSERT INTO
  pedidos_produtos (
    quantidade,
    valor_unitario,
    id_produto,
    id_pedido
  )
VALUES
  (10, 5.99, 1, 1),
  (5, 3.50, 2, 2),
  (2, 8.25, 3, 3),
  (15, 2.99, 4, 4),
  (7, 4.50, 5, 5),
  (3, 7.75, 6, 6),
  (12, 1.99, 7, 7),
  (9, 6.50, 8, 8),
  (4, 3.25, 9, 9),
  (8, 2.50, 10, 10);
commit;
-- -----------------------------------------------------
-- Vendas (insert)
-- -----------------------------------------------------
INSERT INTO
  vendas (
    data_venda,
    id_estabelecimento,
    id_funcionario
  )
VALUES
  ('2023-04-08 15:00:00', 1, 11),
  ('2023-04-08 16:30:00', 2, 12),
  ('2023-04-08 10:15:00', 3, 13),
  ('2023-04-07 18:00:00', 4, 14),
  ('2023-04-06 14:30:00', 5, 15),
  ('2022-03-25 10:30:00', 6, 16),
  ('2022-03-28 15:00:00', 7, 17),
  ('2022-04-01 08:00:00', 8, 18),
  ('2022-04-05 16:45:00', 9, 19),
  ('2022-04-08 11:20:00', 10, 20);
commit;
-- -----------------------------------------------------
-- Vendas_produtos (insert)
-- -----------------------------------------------------
INSERT INTO
  vendas_produtos (
    quantidade,
    valor_unitario,
    id_venda,
    id_produto
  )
VALUES
  (2, 12.50, 1, 2),
  (1, 5.00, 1, 5),
  (3, 7.25, 2, 3),
  (1, 8.99, 3, 1),
  (2, 6.80, 4, 4),
  (2, 19.90, 4, 2),
  (3, 11.99, 4, 3),
  (1, 50.00, 5, 1),
  (4, 8.99, 6, 4),
  (2, 15.50, 6, 2);
commit;
-- -----------------------------------------------------
-- Estabelecimentos_produtos (insert)
-- -----------------------------------------------------
INSERT INTO
  estabelecimentos_produtos (id_estabelecimento, id_produto, quantidade)
VALUES
  (1, 2, 50),
  (2, 5, 100),
  (3, 6, 75),
  (4, 8, 20),
  (5, 1, 60),
  (6, 1, 50),
  (7, 5, 35),
  (8, 3, 20),
  (9, 4, 80),
  (10, 2, 60),
  (1, 3, 25),
  (2, 1, 40),
  (3, 2, 25),
  (4, 7, 10),
  (5, 4, 30),
  (1 , 1, 9),
  (2 , 2, 38),
  (3 , 3, 27),
  (4 , 4, 84),
  (5 , 5, 182),
  (6 , 6, 12),
  (7 , 7, 43),
  (8 , 8, 32),
  (9 , 9, 24),
  (10, 10, 31);
  commit;