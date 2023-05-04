from utilities import *
import psycopg2
from tabulate import tabulate
from datetime import datetime
import os

while True:
    escolhaInicial = menuInicial()

    if escolhaInicial == 0: break
    if not escolhaInicial: continue

    escolhaTabela = None

    # 1 - Cadastro (INSERTS)
    while escolhaInicial == 1 and escolhaTabela != 0:
        escolhaTabela = menuTabelas()
        if escolhaTabela == 0: continue

        if escolhaTabela == 1: # Estabelecimento
            cnpj, telefone = solicitar_inputs('estabelecimento', 'cnpj', 'telefone')
            exec_query('INSERT INTO estabelecimentos (cnpj, telefone) VALUES (%s,%s);', (cnpj, telefone))
        elif escolhaTabela == 2: # Funcionario
            nome, cpf = solicitar_inputs('funcionario', 'nome', 'cpf')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            exec_query("INSERT INTO funcionarios (nome, cpf, id_estabelecimento) VALUES (%s,%s,%s);", (nome, cpf, id_estabelecimento));
        elif escolhaTabela == 3: # Fornecedor
            nome, cnpj, telefone, email = solicitar_inputs('fornecedor', 'nome', 'cnpj', 'telefone', 'email')
            exec_query('INSERT INTO fornecedores (nome, cnpj, telefone, email) VALUES (%s,%s,%s,%s);', (nome, cnpj, telefone, email))
        elif escolhaTabela == 4: # Produto
            nome, descricao = solicitar_inputs('produto', 'nome', 'descricao')
            exec_query('INSERT INTO produtos (nome, descricao)  VALUES (%s,%s)', (nome, descricao))
    # 2 - Consulta (SELECTS)
    while escolhaInicial == 2 and escolhaTabela != 0:
        escolhaTabela = menuTabelas(temTabelasEntidade = True)
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
                                    order by 1 asc
                                """)
            print_tabulado(query, ['ID Estabelecimento', 'Telefone', 'CNPJ'])
        elif escolhaTabela == 2: # Funcionário
            query = query_banco(""" SELECT f.id_funcionario, f.nome,
                                    CASE LENGTH(f.cpf) WHEN 11
                                    THEN SUBSTR(f.cpf,0,4) || '.' || SUBSTR(f.cpf,4,3) || '.' || SUBSTR(f.cpf,7,3) || '-' ||  SUBSTR(f.cpf,10,2)
                                    ELSE f.cpf END,
                                    f.id_estabelecimento,
									CASE LENGTH(e.cnpj) WHEN 14
                                    THEN substr(e.cnpj,1,2) || '.' || SUBSTR(e.cnpj,3,3) || '.' || SUBSTR(e.cnpj,6,3) || '/' || SUBSTR(e.cnpj,9,4) || '-' || SUBSTR(e.cnpj,13,2)
                                    ELSE e.cnpj END CASE
									FROM funcionarios f JOIN estabelecimentos e ON e.id_estabelecimento = f.id_estabelecimento
				                    order by 1 asc
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
				                    order by 1 asc
                                """)
            print_tabulado(query, ['ID Fornecedor', 'Nome', 'CNPJ', 'Telefone', 'E-mail'])
        elif escolhaTabela == 4: # Produto
            query = query_banco("SELECT p.* FROM produtos p order by 1 asc")
            print_tabulado(query, ['ID Produto', 'Nome', 'Descrição'])
        elif escolhaTabela == 5: # Pedido
            query = query_banco(""" SELECT 	ped.id_pedido, COUNT(pedprod.id_produto) AS nr_produtos, 
                                    to_char(ped.data_pedido,'hh:MI dd/mm/YYYY'),
                                    ped.id_estabelecimento, ped.id_funcionario, ped.id_fornecedor
                                    FROM pedidos ped
                                    LEFT JOIN pedidos_produtos pedprod ON pedprod.id_pedido = ped.id_pedido
                                    GROUP BY ped.id_pedido, ped.data_pedido, ped.id_estabelecimento, ped.id_funcionario, ped.id_fornecedor
                                    ORDER BY ped.id_pedido ASC
                                """)
            print_tabulado(query, ['ID Pedido', 'Produtos pedidos', 'Data do pedido', 'ID Estabelecimento', 'ID Funcionario', 'ID Fornecedor'])
        elif escolhaTabela == 6: # Venda
            query = query_banco(""" SELECT	vendas.id_venda, COUNT(venprod.id_produto) AS produtos, 
                                    to_char(vendas.data_venda,'hh:MI dd/mm/YYYY'),
                                    vendas.id_estabelecimento, vendas.id_funcionario
                                    FROM vendas
                                    LEFT JOIN vendas_produtos venprod ON venprod.id_venda = vendas.id_venda
                                    GROUP BY vendas.id_venda, vendas.data_venda, vendas.id_estabelecimento, vendas.id_funcionario
                                    ORDER BY vendas.id_venda
                                """)
            print_tabulado(query, ['ID Venda', 'Produtos vendidos', 'Data da venda', 'ID Estabelecimento', 'ID Funcionario'])
        elif escolhaTabela == 7: #Pedidos produtos
            id_pedido = solicitar_inputs('pedido', 'chave')
            if not id_pedido:
                continue
            query = query_banco(f""" select pp.quantidade, pp.valor_unitario, pr.id_produto, pr.nome, e.id_estabelecimento, 
                                CASE LENGTH(e.cnpj) WHEN 14
                                THEN substr(e.cnpj,1,2) || '.' || SUBSTR(e.cnpj,3,3) || '.' || SUBSTR(e.cnpj,6,3) || '/' || SUBSTR(e.cnpj,9,4) || '-' || SUBSTR(e.cnpj,13,2)
                                ELSE e.cnpj END CASE, 
                                f.id_funcionario, 
                                CASE LENGTH(f.cpf) WHEN 11
                                THEN SUBSTR(f.cpf,0,4) || '.' || SUBSTR(f.cpf,4,3) || '.' || SUBSTR(f.cpf,7,3) || '-' ||  SUBSTR(f.cpf,10,2)
                                ELSE f.cpf END, fo.id_fornecedor,
                                CASE LENGTH(fo.cnpj) WHEN 14
                                THEN SUBSTR(fo.cnpj,1,2) || '.' || SUBSTR(fo.cnpj,3,3) || '.' || SUBSTR(fo.cnpj,6,3) || '/' || SUBSTR(fo.cnpj,9,4) || '-' || SUBSTR(fo.cnpj,13,2)
                                ELSE fo.cnpj END CASE from pedidos_produtos pp join pedidos p on p.id_pedido = pp.id_pedido join produtos pr on pr.id_produto = pp.id_produto join estabelecimentos e on e.id_estabelecimento = p.id_estabelecimento join funcionarios f on f.id_funcionario = p.id_funcionario join fornecedores fo on fo.id_fornecedor = p.id_fornecedor
                                where pp.id_pedido={id_pedido}
                            """)
            print_tabulado(query, ['Quantidade', 'Valor unitário', 'Id Produto', 'Nome Produto', 'ID Estabelecimento','CNPJ Estabelecimento','ID Funcionario','CPF Funcionário','ID Fornecedor','CNPJ Fornecedor'])
        elif escolhaTabela == 8: #Vendas produtos
            id_venda = solicitar_inputs('venda', 'chave')
            if not id_venda:
                continue
            query = query_banco(f""" select vp.quantidade, vp.valor_unitario, pr.id_produto, pr.nome, e.id_estabelecimento, 
                                CASE LENGTH(e.cnpj) WHEN 14
                                THEN substr(e.cnpj,1,2) || '.' || SUBSTR(e.cnpj,3,3) || '.' || SUBSTR(e.cnpj,6,3) || '/' || SUBSTR(e.cnpj,9,4) || '-' || SUBSTR(e.cnpj,13,2)
                                ELSE e.cnpj END CASE, 
                                f.id_funcionario, 
                                CASE LENGTH(f.cpf) WHEN 11
                                THEN SUBSTR(f.cpf,0,4) || '.' || SUBSTR(f.cpf,4,3) || '.' || SUBSTR(f.cpf,7,3) || '-' ||  SUBSTR(f.cpf,10,2)
                                ELSE f.cpf END from vendas_produtos vp join vendas v on v.id_venda = vp.id_venda join produtos pr on pr.id_produto = vp.id_produto join estabelecimentos e on e.id_estabelecimento = v.id_estabelecimento join funcionarios f on f.id_funcionario = v.id_funcionario 
                                where vp.id_venda={id_venda}
                            """)
            print_tabulado(query, ['Quantidade', 'Valor unitário', 'Id Produto', 'Nome Produto', 'ID Estabelecimento','CNPJ Estabelecimento','ID Funcionario','CPF Funcionário'])
        break_line()
        pause()
    
    # 3 - Atualização (UPDATES)
    while escolhaInicial == 3 and escolhaTabela != 0:
        escolhaTabela = menuTabelas()
        if escolhaTabela == 0: continue

        if escolhaTabela == 1: # Estabelecimento
            chave, cnpj, telefone = solicitar_inputs('estabelecimento', 'chave', 'cnpj', 'telefone')
            exec_query("UPDATE estabelecimentos SET telefone = %s, cnpj = %s WHERE id_estabelecimento = %s", (telefone, cnpj, chave))
        elif escolhaTabela == 2: # Funcionário
            chave, nome, cpf = solicitar_inputs('funcionario', 'chave', 'nome', 'cpf')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            exec_query('UPDATE funcionarios SET nome = %s, cpf = %s, id_estabelecimento = %s WHERE id_funcionario = %s', (nome, cpf, id_estabelecimento, chave))
        elif escolhaTabela == 3: # Fornecedor
            chave, nome, cnpj, telefone, email = solicitar_inputs('fornecedor', 'chave', 'nome', 'cnpj', 'telefone', 'email')
            with cursor_banco() as cursor:
                cursor.execute('UPDATE fornecedores SET nome = %s, cnpj = %s, telefone = %s, email = %s WHERE id_fornecedor = %s', (nome, cnpj, telefone, email, chave))
        elif escolhaTabela == 4: # Produto
            chave, nome, descricao = solicitar_inputs('produto', 'chave', 'nome', 'descricao')
            with cursor_banco() as cursor:
                cursor.execute('UPDATE produtos SET nome = %s, descricao = %s WHERE id_produto = %s', (nome, descricao, chave))
        elif escolhaTabela == 5: # Pedidos
            id_pedido = solicitar_inputs('pedido', 'chave')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            id_funcionario = solicitar_inputs('funcionario', 'chave')
            id_fornecedor = solicitar_inputs('fornecedor', 'chave')
            
            with cursor_banco() as cursor:
                cursor.execute("UPDATE pedidos SET id_estabelecimento = %s, id_funcionario = %s, id_fornecedor = %s WHERE id_pedido = %s", (id_estabelecimento, id_funcionario, id_fornecedor, id_pedido))
        elif escolhaTabela == 6: # Vendas
            id_venda = solicitar_inputs('venda', 'chave')
            id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
            id_funcionario = solicitar_inputs('funcionario', 'chave')
            
            with cursor_banco() as cursor:
                cursor.execute("UPDATE vendas SET id_estabelecimento = %s, id_funcionario = %s WHERE id_venda = %s", (id_estabelecimento, id_funcionario, id_venda))

    # 4 - Remoção (DELETES)
    while escolhaInicial == 4 and escolhaTabela != 0:
        escolhaTabela = menuTabelas()
        if escolhaTabela == 0: continue

        if escolhaTabela == 1: # Estabelecimento
            print("ATENÇÃO! Todos os funcionários, pedidos, vendas e produtos vinculados a este estabelecimento serão excluídos!")
            chave = solicitar_inputs('estabelecimento', 'chave')
            with cursor_banco() as cursor:
                cursor.execute(f"DELETE FROM estabelecimentos WHERE id_estabelecimento={chave}")
        elif escolhaTabela == 2: # Funcionário
            print("ATENÇÃO! Todos os pedidos e vendas vinculados a este funcionário serão excluídos!")
            chave = solicitar_inputs('funcionario', 'chave')
            with cursor_banco() as cursor:
                cursor.execute(f"DELETE FROM funcionarios WHERE id_funcionario={chave}")
        elif escolhaTabela == 3: # Fornecedor
            print("ATENÇÃO! Todos os pedidos vinculados a este fornecedor serão excluídos!")
            chave = solicitar_inputs('fornecedor', 'chave')
            with cursor_banco() as cursor:
                cursor.execute(f"DELETE FROM fornecedores WHERE id_fornecedor={chave}")
        elif escolhaTabela == 4: # Produto
            print("ATENÇÃO! Todos os produtos de pedidos, compras ou estabelecimentos vinculados a este serão excluídos!")
            chave = solicitar_inputs('produto', 'chave')
            with cursor_banco() as cursor:
                cursor.execute(f"DELETE FROM produtos WHERE id_produto={chave}")
        elif escolhaTabela == 5: # Pedidos
            print("ATENÇÃO! Todos os registros de produtos pedidos vinculados à este pedido serão excluídos!")
            chave = solicitar_inputs('pedido', 'chave')
            registros = query_banco(f"SELECT pp.quantidade,pp.id_produto,p.id_estabelecimento  FROM pedidos_produtos pp join pedidos p on p.id_pedido = pp.id_pedido where pp.id_pedido={chave}")
            with cursor_banco() as cursor:
                for registro in registros:
                    cursor.execute("UPDATE estabelecimentos_produtos SET quantidade=quantidade-%s WHERE id_estabelecimento= %s AND id_produto=%s",(registro[0],registro[2],registro[1]))
                cursor.execute(f"DELETE FROM pedidos WHERE id_pedido={chave}")
        elif escolhaTabela == 6: # Vendas
            print("ATENÇÃO! Todos os registros de produtos vendidos vinculados à este pedido serão excluídos!")
            chave = solicitar_inputs('venda', 'chave')
            registros = query_banco(f"SELECT vp.quantidade,vp.id_produto,v.id_estabelecimento  FROM vendas_produtos vp join vendas v on v.id_venda = vp.id_venda where vp.id_venda={chave}")
            with cursor_banco() as cursor:
                for registro in registros:
                    cursor.execute("UPDATE estabelecimentos_produtos SET quantidade=quantidade+%s WHERE id_estabelecimento= %s AND id_produto=%s",(registro[0],registro[2],registro[1]))
                cursor.execute(f"DELETE FROM vendas WHERE id_venda={chave}")

    # 5 - Registrar venda
    if escolhaInicial == 5:
        registros = []

        data = datetime.now().strftime('%d/%m/%Y %H:%M')
        id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
        id_funcionario = solicitar_inputs('funcionario', 'chave')

        with cursor_banco() as cursor:
            cursor.execute("INSERT INTO vendas (data_venda, id_estabelecimento, id_funcionario) VALUES (%s, %s, %s) RETURNING id_venda", (data, id_estabelecimento, id_funcionario))
            id_venda = cursor.fetchone()[0]

        while True:
            clear()

            id_produto = int_input("Informe o ID do Produto (0 para finalizar): ")

            # Cancelar
            if id_produto == 0:
                print("Finalizando...")
                break

            # Verificar se o produto existe
            with cursor_banco() as cursor:
                cursor.execute(f"SELECT 1 FROM produtos WHERE id_produto={id_produto}")
                produtoExiste = cursor.fetchone()
            if not produtoExiste:
                print('Produto não existe na base')
                continue
            
            # Verificar se o produto está cadastro no estabelecimento
            with cursor_banco() as cursor:
                cursor.execute("SELECT quantidade FROM estabelecimentos_produtos WHERE id_produto=%s AND id_estabelecimento=%s",(id_produto,id_estabelecimento))
                quantidadeEstoque = cursor.fetchone()[0]
            if not quantidadeEstoque:
                print("Produto não cadastrado no estoque do estabelecimento.")
                continue

            valor_un = float(input("Informe o valor unitário do produto: "))
            quantidadeVendida = int_input("Informe a quantidade de produtos vendidos: ")

            # Validação dos inputs
            if valor_un <= 0 or quantidadeVendida <= 0:
                print('Quantidade pedida invalida.')
                continue

            if quantidadeVendida > quantidadeEstoque:
                print('Quantidade pedida para venda maior que a disponível em estoque')
                print(f'Quantidade disponível: {quantidadeEstoque}')

            registros.append((id_produto, valor_un, quantidadeVendida))

        print(registros)
        with cursor_banco() as cursor:
            for registro in registros:
                id_produto = registro[0]
                valor_un = registro[1]
                quantidadeVendida = registro[2]
                cursor.execute("INSERT INTO vendas_produtos (quantidade, valor_unitario, id_venda, id_produto) VALUES (%s, %s, %s, %s)", (quantidadeVendida, valor_un, id_venda, id_produto))
                cursor.execute("UPDATE estabelecimentos_produtos SET quantidade=quantidade-%s WHERE id_estabelecimento= %s AND id_produto=%s",(quantidadeVendida,id_estabelecimento,id_produto))

    # 6 - Realizar pedido
    if escolhaInicial == 6:
        registros = []

        data = datetime.now().strftime('%d/%m/%Y %H:%M')
        id_estabelecimento = solicitar_inputs('estabelecimento', 'chave')
        id_funcionario = solicitar_inputs('funcionario', 'chave')
        id_fornecedor = solicitar_inputs('fornecedor', 'chave')

        with cursor_banco() as cursor:
            cursor.execute("INSERT INTO pedidos (data_pedido, id_estabelecimento, id_funcionario, id_fornecedor) VALUES (%s, %s, %s, %s) RETURNING id_pedido", (data, id_estabelecimento, id_funcionario, id_fornecedor));
            id_pedido = cursor.fetchone()[0]

        while True:
            clear()

            id_produto = int_input("Informe o ID do Produto (0 para finalizar): ")

            # Cancelar
            if id_produto == 0:
                print("Finalizando...")
                break

            # Verificar se o produto existe
            with cursor_banco() as cursor:
                cursor.execute(f"SELECT 1 FROM produtos WHERE id_produto={id_produto}",)
                produtoExiste = cursor.fetchone()[0]
            if not produtoExiste:
                print('Produto não existe na base')
                continue
            
            # Verificar se o produto está cadastro no estabelecimento
            with cursor_banco() as cursor:
                cursor.execute("SELECT quantidade FROM estabelecimentos_produtos WHERE id_produto=%s AND id_estabelecimento=%s",(id_produto,id_estabelecimento ))
                produtoCadastradoEstabelecimento = cursor.fetchone()[0]
            if not produtoCadastradoEstabelecimento:
                cursor.execute("INSERT INTO estabelecimentos_produtos VALUES (%s,%s, 0);",(id_estabelecimento, id_produto))

            valor_un = float(input("Informe o valor unitário do produto: "))
            quantidadePedida = int_input("Informe a quantidade de produtos comprados: ")

            # Validação dos inputs
            if valor_un <= 0 or quantidadePedida <= 0:
                print('Quantidade pedida invalida.')
                continue

            registros.append((id_produto, valor_un, quantidadePedida))

        print(registros)
        with cursor_banco() as cursor:
            for registro in registros:
                id_produto = registro[0]
                valor_un = registro[1]
                quantidadePedida = registro[2]
                cursor.execute("INSERT INTO pedidos_produtos (quantidade, valor_unitario, id_produto, id_pedido) VALUES (%s,%s,%s,%s)",(quantidadePedida, valor_un, id_produto, id_pedido))
                cursor.execute("UPDATE estabelecimentos_produtos SET quantidade=quantidade+%s WHERE id_estabelecimento=%s AND id_produto=%s",(quantidadePedida,id_estabelecimento,id_produto))


    # 7 - Relatórios
    escolhaRelatorio = None
    while escolhaInicial == 7 and escolhaRelatorio != 0:
        escolhaRelatorio = menuRelatorios()
        if escolhaRelatorio == 0: continue
        break_line()

        # Adicionar filtros

        if escolhaRelatorio == 1: # Produtos disponíveis em cada estabelecimento
            id_estabelecimento = int_input('Informe o ID do estabelecimento (0 para todos estabelecimentos): ')
            query = query_banco(f""" SELECT estab.id_estabelecimento, estab.cnpj, prod.id_produto, prod.nome,sum(prod.id_produto)
                                    FROM produtos prod
                                    INNER JOIN estabelecimentos_produtos estab_prod
                                    ON estab_prod.id_produto = prod.id_produto
                                    INNER JOIN estabelecimentos estab
                                    ON estab.id_estabelecimento = estab_prod.id_estabelecimento
									where (estab.id_estabelecimento={id_estabelecimento} or 0={id_estabelecimento})
                                    GROUP BY estab.id_estabelecimento, estab.cnpj, prod.id_produto, prod.nome
									order by 1 asc
                                """)
            print_tabulado(query, ['ID Estabelecimento', 'CNPJ','ID Produto','Nome Produto','Quantidade de produtos'])
        elif escolhaRelatorio == 2: # Vendas por funcionário
            id_funcionario = int_input('Informe o ID do funcionário (0 para todos funcionários): ')
            query = query_banco(f""" SELECT f.id_funcionario, f.nome, count(v.id_venda) AS qtd_vendas, SUM(v_prod.valor_unitario * v_prod.quantidade) AS valor_arrecadado, to_char(v.data_venda,'MM/YYYY')
                                    FROM funcionarios f
                                    INNER JOIN vendas v
                                    ON v.id_funcionario = f.id_funcionario
                                    INNER JOIN vendas_produtos v_prod
                                    ON v_prod.id_venda = v.id_venda
                                    where (f.id_funcionario={id_funcionario} or 0={id_funcionario})
                                    GROUP BY f.id_funcionario, f.nome, to_char(v.data_venda,'MM/YYYY')
									order by 1 asc
                                """)
            print_tabulado(query, ['ID Funcionario', 'Nome', 'Quantidade de vendas', 'Valor arrecadado','Mês/Ano'])
        elif escolhaRelatorio == 3: # Compras por fornecedor
            id_fornecedor = int_input('Informe o ID do fornecedor (0 para todos fornecedores): ')
            query = query_banco(f""" SELECT f.nome, count(ped.id_pedido) AS qtd_pedidos, sum(ped_prod.valor_unitario * ped_prod.quantidade) AS valor_pago, to_char(ped.data_pedido,'MM/YYYY')
                                    FROM fornecedores f
                                    INNER JOIN pedidos ped
                                    ON ped.id_fornecedor = f.id_fornecedor
                                    INNER JOIN pedidos_produtos ped_prod
                                    ON ped_prod.id_pedido = ped.id_pedido
                                    where (f.id_fornecedor={id_fornecedor} or 0={id_fornecedor})
                                    GROUP BY f.nome, to_char(ped.data_pedido,'MM/YYYY')
                                """)
            print_tabulado(query, ['Fornecedor', 'Quantidade de pedidos', 'Valor pago','Mês/Ano'])
        
        break_line()
        pause()
