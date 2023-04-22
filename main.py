from utilities import *
import pyodbc
from tabulate import tabulate
from datetime import datetime
import os

# Ver com Rodrigo
# Operações de negócio e relatórios -> CRUD das tabelas associativas

# -> Cancelar venda e cancelar pedido (acho que não precisa)
# -> Relatórios com condicionais? Ex.: Vendas por funcionario em certa data
# -> Validação de CNPJ e CPF
#       -> Após isso, precisa verificar os "solicitar_inputs()", pois caso venha um valor invalidado, precisa cancelar o processo
#       Ex.: CNPJ invalido no cadastro de estabelecimento, retorna uma tupla (,'23123123'), o que vai causar erro no insert, portanto deve ser validado
#       -> Essa validação também deve ser feito para os UPDATES e DELETES, pois quebra a execução do programa

# Adicionar consulta de estoque

while True:
    escolhaInicial = menuInicial()
    if escolhaInicial == 0: break

    escolhaTabela = None

    # 1 - Cadastro (INSERTS)
    while escolhaInicial == 1 and escolhaTabela != 0:
        escolhaTabela = menuTabelas()
        if escolhaTabela == 0: continue

        if escolhaTabela == 1: # Estabelecimento
            cnpj, telefone = solicitar_inputs('estabelecimento', 'cnpj', 'telefone')
            query_banco(f"INSERT INTO estabelecimentos (telefone, cnpj) VALUES ({cnpj}, {telefone});")
        elif escolhaTabela == 2: # Funcionário
            nome, cpf = solicitar_inputs('funcionario', 'nome', 'cpf')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            with cursor_banco() as cursor:
                cursor.execute("INSERT INTO funcionarios (nome, cpf, id_estabelecimento) VALUES (?, ?, ?)", nome, cpf, id_estabelecimento)
        elif escolhaTabela == 3: # Fornecedor
            nome, cnpj, telefone, email = solicitar_inputs('fornecedor', 'nome', 'cnpj', 'telefone', 'email')
            with connect_banco() as cursor:
                cursor.execute('INSERT INTO fornecedores (nome, cnpj, telefone, email) VALUES (?, ?, ?, ?)', nome, cnpj, telefone, email)
        elif escolhaTabela == 4: # Produto
            nome, descricao = solicitar_inputs('produto', 'nome', 'descricao')
            with connect_banco() as cursor:
                cursor.execute('INSERT INTO produtos (nome, descricao)  VALUES (?, ?)', nome, descricao)
        elif escolhaTabela == 5: # Pedidos
            data = datetime.now().strftime('%d/%m/%Y %H:%M')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            id_funcionario = solicitar_inputs('funcionario', 'chave')
            id_fornecedor = solicitar_inputs('fornecedor', 'chave')
            
            with cursor_banco() as cursor:
                cursor.execute("INSERT INTO pedidos (data_pedido, id_estabelecimento, id_funcionario, id_fornecedor) VALUES (?, ?, ?, ?) RETURNING id_pedido", data, id_estabelecimento, id_funcionario, id_fornecedor)
                # Fazer um código para mostrar o ID do pedido criado, para que o usuário possa referenciá-lo nas operações de negócios.
        elif escolhaTabela == 6: # Vendas
            data = datetime.now().strftime('%d/%m/%Y %H:%M')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            id_funcionario = solicitar_inputs('funcionario', 'chave')
            
            with cursor_banco() as cursor:
                cursor.execute("INSERT INTO vendas (data_venda, id_estabelecimento, id_funcionario) VALUES (?, ?, ?)", data, id_estabelecimento, id_funcionario)
                # Fazer um código para mostrar o ID do pedido criado, para que o usuário possa referenciá-lo nas operações de negócios.
    
    # 2 - Consulta (SELECTS)
    while escolhaInicial == 2 and escolhaTabela != 0:
        escolhaTabela = menuTabelas()
        if escolhaTabela == 0: continue

        break_line()
        if escolhaTabela == 1: # Estabelecimento
            query = query_banco(""" SELECT e.id_estabelecimento,
                                    CASE LENGTH(e.telefone) WHEN 11
                                    THEN '(' || substr(e.telefone,0,3) || ') ' || SUBSTR(e.telefone,3,5) || '-' || SUBSTR(e.telefone,8,15)
                                    ELSE e.telefone END CASE,
                                    CASE LENGTH(e.cnpj) WHEN 14
                                    THEN substr(e.cnpj,1,2) || '.' || SUBSTR(e.cnpj,3,3) || '.' || SUBSTR(e.cnpj,6,3) || '/' || SUBSTR(e.cnpj,9,4) || '-' || SUBSTR(e.cnpj,13,2)
                                    ELSE e.cnpj END CASE FROM estabelecimentos e
                                    
                                """)
            print_tabulado(query, ['ID Estabelecimento', 'Telefone', 'CNPJ'])
        elif escolhaTabela == 2: # Funcionário
            query = query_banco(""" SELECT f.id_funcionario, f.nome,
                                    CASE LENGTH(f.cpf) WHEN 11
                                    THEN SUBSTR(f.cpf,0,4) || '.' || SUBSTR(f.cpf,4,3) || '.' || SUBSTR(f.cpf,7,3) || '-' ||  SUBSTR(f.cpf,10,2)
                                    ELSE f.cpf END,
                                    f.id_estabelecimento,
                                    e.cnpj FROM funcionarios f JOIN estabelecimentos e ON e.id_estabelecimento = f.id_estabelecimento
                                """)
            print_tabulado(query, ['ID Funcionário', 'Nome', 'CPF', 'ID Estabelecimento', 'CNPJ Estabelecimento'])
        elif escolhaTabela == 3: # Fornecedor
            query = query_banco(""" SELECT fo.id_fornecedor, fo.nome,
                                    CASE LENGTH(fo.cnpj) WHEN 14
                                    THEN SUBSTR(fo.cnpj,1,2) || '.' || SUBSTR(fo.cnpj,3,3) || '.' || SUBSTR(fo.cnpj,6,3) || '/' || SUBSTR(fo.cnpj,9,4) || '-' || SUBSTR(fo.cnpj,13,2)
                                    ELSE fo.cnpj END CASE,
                                    CASE LENGTH(fo.telefone) WHEN 11
                                    THEN '(' || substr(fo.telefone,0,3) || ') ' || substr(fo.telefone,3,5) || '-' || substr(fo.telefone,8,15)
                                    ELSE fo.telefone END CASE,
                                    fo.email FROM fornecedores fo
                                """)
            print_tabulado(query, ['ID Fornecedor', 'Nome', 'CNPJ', 'Telefone', 'E-mail'])
        elif escolhaTabela == 4: # Produto
            query = query_banco("SELECT p.* FROM produtos p")
            print_tabulado(query, ['ID Produto', 'Nome', 'Descrição'])
        elif escolhaTabela == 5: # Pedido
            query = query_banco(""" SELECT 	ped.id_pedido, COUNT(pedprod.id_produto) AS produtos, ped.data_pedido,
                                            ped.id_estabelecimento, ped.id_funcionario, ped.id_fornecedor
                                    FROM pedidos ped
                                    LEFT JOIN pedidos_produtos pedprod ON pedprod.id_pedido = ped.id_pedido
                                    GROUP BY ped.id_pedido, ped.data_pedido, ped.id_estabelecimento, ped.id_funcionario, ped.id_fornecedor
                                    ORDER BY ped.id_pedido ASC
                                """)
            print_tabulado(query, ['ID Pedido', 'Produtos pedidos', 'Data do pedido', 'ID Estabelecimento', 'ID Funcionario', 'ID Fornecedor'])
        elif escolhaTabela == 6: # Venda
            query = query_banco(""" SELECT	vendas.id_venda, COUNT(venprod.id_produto) AS produtos, vendas.data_venda,
                                    vendas.id_estabelecimento, vendas.id_funcionario
                                    FROM vendas
                                    LEFT JOIN vendas_produtos venprod ON venprod.id_venda = vendas.id_venda
                                    GROUP BY vendas.id_venda, vendas.data_venda, vendas.id_estabelecimento, vendas.id_funcionario
                                    ORDER BY vendas.id_venda
                                """)
            print_tabulado(query, ['ID Venda', 'Produtos vendidos', 'Data da venda', 'ID Estabelecimento', 'ID Funcionario'])

        break_line()
        pause()
    
    # 3 - Atualização (UPDATES)
    while escolhaInicial == 3 and escolhaTabela != 0:
        escolhaTabela = menuTabelas()
        if escolhaTabela == 0: continue

        if escolhaTabela == 1: # Estabelecimento
            chave, cnpj, telefone = solicitar_inputs('estabelecimento', 'chave', 'cnpj', 'telefone')
            with cursor_banco() as cursor:
                cursor.execute(f"UPDATE estabelecimentos SET telefone = ?, cnpj = ? WHERE id_estabelecimento = ?", telefone, cnpj, chave)
        elif escolhaTabela == 2: # Funcionário
            chave, nome, cpf = solicitar_inputs('funcionario', 'chave', 'nome', 'cpf')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            with cursor_banco() as cursor:
                cursor.execute('UPDATE funcionarios SET nome = ?, cpf = ?, id_estabelecimento = ? WHERE id_funcionario = ?', nome, cpf, id_estabelecimento, chave)
        elif escolhaTabela == 3: # Fornecedor
            chave, nome, cnpj, telefone, email = solicitar_inputs('fornecedor', 'chave', 'nome', 'cnpj', 'telefone', 'email')
            with cursor_banco() as cursor:
                cursor.execute('UPDATE fornecedores SET nome = ?, cnpj = ?, telefone = ?, email = ? WHERE id_fornecedor = ?', nome, cnpj, telefone, email, chave)
        elif escolhaTabela == 4: # Produto
            chave, nome, descricao = solicitar_inputs('produto', 'chave', 'nome', 'descricao')
            with cursor_banco() as cursor:
                cursor.execute(f'UPDATE produtos SET nome = ?, descricao = ? WHERE id_produto = ?', nome, descricao, chave)
        elif escolhaTabela == 5: # Pedidos
            id_pedido = solicitar_inputs('pedido', 'chave')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            id_funcionario = solicitar_inputs('funcionario', 'chave')
            id_fornecedor = solicitar_inputs('fornecedor', 'chave')
            
            with cursor_banco() as cursor:
                cursor.execute("UPDATE pedidos SET id_estabelecimento = ?, id_funcionario = ?, id_fornecedor = ? WHERE id_pedido = ?", id_estabelecimento, id_funcionario, id_fornecedor, id_pedido)
        elif escolhaTabela == 6: # Vendas
            id_venda = solicitar_inputs('venda', 'chave')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            id_funcionario = solicitar_inputs('funcionario', 'chave')
            
            with cursor_banco() as cursor:
                cursor.execute("UPDATE vendas SET id_estabelecimento = ?, id_funcionario = ? WHERE id_venda = ?", id_estabelecimento, id_funcionario, id_venda)

    # 4 - Remoção (DELETES)
    while escolhaInicial == 4 and escolhaTabela != 0:
        escolhaTabela = menuTabelas()
        if escolhaTabela == 0: continue

        if escolhaTabela == 1: # Estabelecimento
            print("ATENÇÃO! Todos os funcionários, pedidos, vendas e produtos vinculados a este estabelecimento serão excluídos!")
            chave = solicitar_inputs('estabelecimento', 'chave')
            with cursor_banco() as cursor:
                cursor.execute("DELETE FROM estabelecimentos WHERE id_estabelecimento=?", chave)
        elif escolhaTabela == 2: # Funcionário
            print("ATENÇÃO! Todos os pedidos e vendas vinculados a este funcionário serão excluídos!")
            chave = solicitar_inputs('funcionario', 'chave')
            with cursor_banco() as cursor:
                cursor.execute("DELETE FROM funcionarios WHERE id_funcionario=?", chave)
        elif escolhaTabela == 3: # Fornecedor
            print("ATENÇÃO! Todos os pedidos vinculados a este fornecedor serão excluídos!")
            chave = solicitar_inputs('fornecedor', 'chave')
            with cursor_banco() as cursor:
                cursor.execute("DELETE FROM fornecedores WHERE id_fornecedor=?", chave)
        elif escolhaTabela == 4: # Produto
            print("ATENÇÃO! Todos os produtos de pedidos, compras ou estabelecimentos vinculados a este serão excluídos!")
            chave = solicitar_inputs('produto', 'chave')
            with cursor_banco() as cursor:
                cursor.execute("DELETE FROM produtos WHERE id_produto=?", chave)
        elif escolhaTabela == 5: # Pedidos
            pass
        elif escolhaTabela == 6: # Vendas
            pass

    # 5 - Registrar venda
    # Se o produto não existe na estabelecimento produtos ou quantidadeVendida < quantidadeEstoque, bloqueia a venda, não permite
    # Avisa e volta para cadastro de produtos, (da um continue)
    
    # Operações de negócios -> CRUD das vendas
    if escolhaInicial == 5:
        print('Venda')
        pass

    # 6 - Realizar pedido
    # Operações de negócios -> CRUD dos pedidos
    if escolhaInicial == 6:
        contador = 0
        registroHistorico = []
        while True: # Cadastro de produtos no pedido
            clear()
            id_produto = int_input("Informe o ID do Produto (0 para cancelar): ")
            valor_un = float(input("Informe o valor unitário do produto: "))
            quantidadePedida = int_input("Informe a quantidade de produtos comprados: ")

            # Validação dos inputs
            if valor_un <= 0:
                print('Quantidade pedida invalida.')
                continue
            if quantidadePedida <= 0:
                print('Quantidade pedida invalida.')
                continue
            
            # Confirmação
            print(f'ID Produto: {id_produto}\nValor un.: {valor_un}\nQuantidade: {quantidadePedida}\n\nDeseja confirmar?')
            escolha = int_input('1 - Sim.\n2 - Não.\n3 - Cancelar pedido.')
            if inserirMaisProduto == 2:
                continue
            if inserirMaisProduto == 3:
                for registro in registroHistorico:
                    with cursor_banco() as cursor:
                        cursor.execute(f"SELECT quantidade FROM estabelecimentos_produtos WHERE id_produto={registro[0]} AND id_estabelecimento={id_estabelecimento}")
                        quantidadeAtual = cursor.fetchone()[0] - registro[1]
                    query_banco(f"UPDATE estabelecimentos_produtos SET quantidade={quantidadeAtual} WHERE id_estabelecimento={id_estabelecimento} AND id_produto={id_produto}")
                query_banco(f'DELETE FROM pedidos WHERE id_pedido = {id_pedido}')
                break


            # Seleciona a quantidade atual em estoque -> mudar nome da variável de quantidadeAtual para estoqueAtual
            with cursor_banco() as cursor:
                cursor.execute(f"SELECT quantidade FROM estabelecimentos_produtos WHERE id_produto={id_produto} AND id_estabelecimento={id_estabelecimento}")
                quantidadeAtual = cursor.fetchone()
            if quantidadeAtual:
                quantidadeAtual = quantidadeAtual[0]

            # Produto não cadastrado neste estabelecimento
            if not quantidadeAtual:
                with cursor_banco() as cursor: # MUDAR O SELECT PARA PRODUTOS
                    cursor.execute(f"SELECT quantidade FROM estabelecimentos_produtos WHERE id_produto={id_produto}")
                    quantidadeAtual = cursor.fetchone()[0]
                if not quantidadeAtual: # Produto não cadastrado na base -> não está cadastrado, abrir margem para cadastrar na tabela produtos depois e inserir no pedido
                    print('Produto não existe. Deseja cadastrar?')
                    produtoExiste = False
                else:
                    print('Produto não está cadastrado neste estabelecimento, deseja associar o produto?')
                    # Cadastrar produto no estabelecimento_produtos com estoque zerados
                    produtoExiste = True
    
                escolha = int_input('1 - Cadastrar produto.\n2 - Finalizar pedido.\n3 - Cancelar pedido.')
                if escolha == 1:
                    if produtoExiste:
                        pass
                    if not produtoExiste:
                        nome, descricao = solicitar_inputs('produto', 'nome', 'descricao')
                        query_banco(f'INSERT INTO produtos (nome, descricao)  VALUES ({nome}, {descricao});')
                if escolha == 2:
                    break
                if escolha == 3:
                    for registro in registroHistorico:
                        with cursor_banco() as cursor:
                            cursor.execute(f"SELECT quantidade FROM estabelecimentos_produtos WHERE id_produto={registro[0]} AND id_estabelecimento={id_estabelecimento}")
                            quantidadeAtual = cursor.fetchone()[0]  - registro[1]
                        query_banco(f"UPDATE estabelecimentos_produtos SET quantidade={quantidadeAtual} WHERE id_estabelecimento={id_estabelecimento} AND id_produto={id_produto}")
                    query_banco(f'DELETE FROM pedidos WHERE id_pedido = {id_pedido}')
                    break
            
            # Produto cadastrado e inserido no pedido
            with cursor_banco() as cursor:
                cursor.execute("INSERT INTO pedidos_produtos (quantidade, valor_unitario, id_produto, id_pedido) VALUES (?, ?, ?, ?) RETURNING id_produto;", quantidadePedida, valor_un, id_produto, id_pedido)
                id_produto = cursor.fetchone()[0]
            
            registroHistorico.append((id_produto, quantidadePedida))

            # Estoque do produto atualizado
            quantidadeAtual += quantidadePedida
            query_banco(f"UPDATE estabelecimentos_produtos SET quantidade={quantidadeAtual} WHERE id_estabelecimento={id_estabelecimento} AND id_produto={id_produto}")
            contador += 1

            # Cadastro de mais produtos ou cancelamento da compra
            inserirMaisProduto = int_input("Deseja inserir mais um produto nesse pedido?\n1 - Sim\n2 - Não\n3 - Cancelar compra ")
            if inserirMaisProduto == 2:
                break
            if inserirMaisProduto == 3:
                for registro in registroHistorico:
                    with cursor_banco() as cursor:
                        cursor.execute(f"SELECT quantidade FROM estabelecimentos_produtos WHERE id_produto={registro[0]} AND id_estabelecimento={id_estabelecimento}")
                        quantidadeAtual = cursor.fetchone()[0] - registro[1]
                    query_banco(f"UPDATE estabelecimentos_produtos SET quantidade={quantidadeAtual} WHERE id_estabelecimento={id_estabelecimento} AND id_produto={id_produto}")
                query_banco(f'DELETE FROM pedidos WHERE id_pedido = {id_pedido}')
                break
            
            print(5)
        if contador == 0 and not quantidadeAtual:
            print('Nenhum produto cadastrado no pedido, cancelando ordem de compra.')
            query_banco(f"DELETE FROM pedidos WHERE id_pedido={id_pedido}")

        # Tirar cancelamento durante cadastro


    # 7 - Relatórios
    escolhaRelatorio = None
    while escolhaInicial == 7 and escolhaRelatorio != 0:
        escolhaRelatorio = menuRelatorios()
        if escolhaRelatorio == 0: continue
        break_line()

        # Adicionar filtros

        if escolhaRelatorio == 1: # Produtos disponíveis em cada estabelecimento -> Filtro por estabelecimento, detalhar produtos
            query = query_banco(""" SELECT estab.id_estabelecimento, estab.cnpj, sum(prod.id_produto)
                                    FROM produtos prod
                                    INNER JOIN estabelecimentos_produtos estab_prod
                                    ON estab_prod.id_produto = prod.id_produto
                                    INNER JOIN estabelecimentos estab
                                    ON estab.id_estabelecimento = estab_prod.id_estabelecimento
                                    GROUP BY estab.id_estabelecimento, estab.cnpj
                                """)
            print_tabulado(query, ['ID Estabelecimento', 'CNPJ', 'Quantidade de produtos'])
        elif escolhaRelatorio == 2: # Vendas por funcionário -> Filtro por data e filtro por funcionario (detalhar produtos)
            query = query_banco(""" SELECT f.id_funcionario, f.nome, SUM(v_prod.quantidade) AS quantidade, SUM(v_prod.valor_unitario * v_prod.quantidade) AS valor_arrecadado
                                    FROM funcionarios f
                                    INNER JOIN vendas v
                                    ON v.id_funcionario = f.id_funcionario
                                    INNER JOIN vendas_produtos v_prod
                                    ON v_prod.id_venda = v.id_venda
                                    GROUP BY f.id_funcionario, f.nome
                                """)
            print_tabulado(query, ['ID Funcionario', 'Nome', 'Quantidade vendida', 'Valor arrecadado'])
        elif escolhaRelatorio == 3: # Compras por fornecedor -> Filtro por data e por fornecedor (detalhar produtos)
            query = query_banco(""" SELECT f.nome, sum(ped_prod.quantidade) AS produtos, sum(ped_prod.valor_unitario * ped_prod.quantidade) AS valor_pago
                                    FROM fornecedores f
                                    INNER JOIN pedidos ped
                                    ON ped.id_fornecedor = f.id_fornecedor
                                    INNER JOIN pedidos_produtos ped_prod
                                    ON ped_prod.id_pedido = ped.id_pedido
                                    GROUP BY f.nome
                                """)
            print_tabulado(query, ['Fornecedor', 'Produtos comprados', 'Valor pago'])
        
        break_line()
        pause()
