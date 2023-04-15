import psycopg2
from tabulate import tabulate
from datetime import datetime


def menu():
    print("Informe a opção desejada:")
    print("1 - Estabelecimentos")
    print("2 - Funcionários")
    print("3 - Fornecedores")
    print("4 - Produtos")
    print("5 - Pedidos")
    print("6 - Vendas")
    print("7 - Relatórios")
    print("0 - Sair")


def menuCRUD():
    print("Informe a opção desejada:")
    print("1 - Mostrar todos")
    print("2 - Adicionar")
    print("3 - Remover")
    print("4 - Editar")
    print("0 - Voltar")


def menuRelatorios():
    print("Informe o relatório desejado:")
    print("1 - Produtos disponíveis em cada estabelecimento")
    print("2 - Vendas por funcionário")
    print("3 - Compras por funcionário")
    print("0 - Voltar")


conn = psycopg2.connect("dbname=db_atacadista user=postgres password=admin") #Nome do banco, usuário e senha
cursor = conn.cursor()

menu()
opcao = int(input("Digite sua opção: "))
while opcao != 0:
    if opcao == 1:
        print("Estabelecimentos")
        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                #Mostrar todos
                cursor.execute(
                    "select e.id_estabelecimento, case length(e.cnpj) when 14 then substr(e.cnpj,1,2) || '.' || substr("
                    "e.cnpj,3,3) || '.' || substr(e.cnpj,6,3) || '/' || substr(e.cnpj,9,4) || '-' || substr(e.cnpj,13,"
                    "2) else e.cnpj end case, case length(e.telefone) when 11 then '(' || substr(e.telefone,0,3) || ') ' "
                    "|| substr(e.telefone,3,5) || '-' || substr(e.telefone,8,15)  else e.telefone end case from "
                    "estabelecimentos e")
                query = cursor.fetchall()
                header = ['ID Estabelecimento', 'Telefone', 'CNPJ']
                print(tabulate(query, headers=header))
            elif opcaoCRUD == 2:
                #Adicionar"
                cnpj = input("Informe o CNPJ do Estabelecimento: ")
                telefone = input("Informe o telefone do Estabelecimento (com DDD): ")
                cursor.execute(
                    "INSERT INTO estabelecimentos (telefone, cnpj) VALUES (%s, %s);",
                    (telefone, cnpj))
                conn.commit()
            elif opcaoCRUD == 3:
                #Remover
                print("ATENÇÃO! Todos os funcionários, pedidos, vendas e produtos vinculados a este estabelecimento "
                      "serão excluídos!")
                chave = int(input("Digite o ID do estabelecimento a ser excluído: "))
                cursor.execute("DELETE FROM estabelecimentos WHERE id_estabelecimento=%s", (chave,))
                conn.commit()
            elif opcaoCRUD == 4:
                #Editar
                chave = int(input("Digite o ID do estabelecimento a ser alterado: "))
                cnpj = input("Informe o CNPJ do Estabelecimento: ")
                telefone = input("Informe o telefone do Estabelecimento (com DDD): ")
                cursor.execute(
                    "UPDATE estabelecimentos SET telefone = %s, cnpj = %s WHERE id_estabelecimento = %s",
                    (telefone, cnpj, chave))
                conn.commit()
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))

    if opcao == 2:
        print("Funcionários")
        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
                cursor.execute(
                    "select f.id_funcionario, f.nome, case length(f.cpf) when 11 then substr(f.cpf,0,4) || '.' || substr(f.cpf,4,3) || '.' || substr(f.cpf,7,3) || '-' ||  substr(f.cpf,10,2)  else f.cpf end, f.id_estabelecimento, e.cnpj from funcionarios f join estabelecimentos e on e.id_estabelecimento = f.id_estabelecimento")
                query = cursor.fetchall()
                header = ['ID Funcionário', 'Nome', 'CPF', 'ID Estabelecimento', 'CNPJ Estabelecimento']
                print(tabulate(query, headers=header))
            elif opcaoCRUD == 2:
                # Adicionar"
                nome = input("Informe o Nome completo do Funcionário: ")
                cpf = input("Informe o CPF do Funcionário: ")
                id_estabelecimento = int(input("Informe o ID do Estabelecimento que o Funcionário trabalha: "))
                cursor.execute(
                    "INSERT INTO funcionarios (nome, cpf, id_estabelecimento) VALUES (%s, %s, %s);",
                    (nome, cpf, id_estabelecimento))
                conn.commit()
            elif opcaoCRUD == 3:
                # Remover
                print("ATENÇÃO! Todos os pedidos e vendas vinculados a este funcionário "
                      "serão excluídos!")
                chave = int(input("Digite o ID do funcionário a ser excluído: "))
                cursor.execute("DELETE FROM funcionarios WHERE id_funcionario=%s", (chave,))
                conn.commit()
            elif opcaoCRUD == 4:
                # Editar
                chave = int(input("Digite o ID do funcionário a ser alterado: "))
                nome = input("Informe o Nome completo do Funcionário: ")
                cpf = input("Informe o CPF do Funcionário: ")
                id_estabelecimento = int(input("Informe o ID do Estabelecimento que o Funcionário trabalha: "))
                cursor.execute(
                    "UPDATE funcionarios SET nome = %s, cpf = %s, id_estabelecimento = %s WHERE id_funcionario = %s",
                    (nome, cpf, id_estabelecimento, chave))
                conn.commit()
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))

    if opcao == 3:
        print("Fornecedores")

        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
                cursor.execute("select fo.id_fornecedor, fo.nome, case length(fo.cnpj) when 14 then  substr(fo.cnpj,1,2) || '.' || substr(fo.cnpj,3,3) || '.' || substr(fo.cnpj,6,3) || '/' || substr(fo.cnpj,9,4) || '-' || substr(fo.cnpj,13,2) else fo.cnpj end case, case length(fo.telefone) when 11 then '(' || substr(fo.telefone,0,3) || ') ' || substr(fo.telefone,3,5) || '-' || substr(fo.telefone,8,15)  else fo.telefone end case, fo.email from fornecedores fo")
                query = cursor.fetchall()
                header = ['ID Fornecedor', 'Nome', 'CNPJ', 'Telefone', 'E-mail']
                print(tabulate(query, headers=header))
            elif opcaoCRUD == 2:
                # Adicionar"
                nome = input("Informe o Nome completo do Fornecedor: ")
                cnpj = input("Informe o CNPJ do Fornecedor: ")
                telefone = input("Informe o Telefone do Fornecedor: ")
                email = input("Informe o E-mail do Fornecedor: ")
                cursor.execute(
                    "INSERT INTO fornecedores (nome, cnpj, telefone, email) VALUES (%s, %s, %s, %s);",
                    (nome, cnpj, telefone,email))
                conn.commit()
            elif opcaoCRUD == 3:
                # Remover
                print("ATENÇÃO! Todos os pedidos vinculados a este fornecedor "
                      "serão excluídos!")
                chave = int(input("Digite o ID do fornecedor a ser excluído: "))
                cursor.execute("DELETE FROM fornecedores WHERE id_fornecedor=%s", (chave,))
                conn.commit()
            elif opcaoCRUD == 4:
                # Editar
                chave = int(input("Digite o ID do fornecedor a ser alterado: "))
                nome = input("Informe o Nome completo do Fornecedor: ")
                cnpj = input("Informe o CNPJ do Fornecedor: ")
                telefone = input("Informe o Telefone do Fornecedor: ")
                email = input("Informe o E-mail do Fornecedor: ")
                cursor.execute(
                    "UPDATE fornecedores SET nome = %s, cnpj = %s, telefone = %s, email = %s WHERE id_fornecedor = %s",
                    (nome, cnpj, telefone,email,chave))
                conn.commit()
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))

    if opcao == 4:
        print("Produtos")
        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
                cursor.execute(
                    "select p.* from produtos p")
                query = cursor.fetchall()
                header = ['ID Produto', 'Nome', 'Descrição']
                print(tabulate(query, headers=header))
            elif opcaoCRUD == 2:
                # Adicionar"
                nome = input("Informe o Nome do produto: ")
                descricao = input("Informe a descricao do produto: ")
                cursor.execute(
                    "INSERT INTO produtos (nome, descricao)  VALUES (%s, %s);",
                    (nome, descricao))
                conn.commit()
            elif opcaoCRUD == 3:
                # Remover
                print("ATENÇÃO! Todos os produtos de pedidos, compras ou estabelecimentos vinculados a este "
                      "serão excluídos!")
                chave = int(input("Digite o ID do produto a ser excluído: "))
                cursor.execute("DELETE FROM produtos WHERE id_produto=%s", (chave,))
                conn.commit()
            elif opcaoCRUD == 4:
                # Editar
                chave = int(input("Digite o ID do produto a ser alterado: "))
                nome = input("Informe o Nome do produto: ")
                descricao = input("Informe a descricao do produto: ")
                cursor.execute(
                    "UPDATE produtos SET nome = %s, descricao = %s WHERE id_fornecedor = %s",
                    (nome, descricao, chave))
                conn.commit()
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))

    if opcao == 5:
        print("Pedidos")

        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
                cursor.execute("select p.id_pedido, to_char(p.data_pedido,'dd/mm/YYYY hh:ss'), p.id_estabelecimento, case length(e.cnpj) when 14 then substr(e.cnpj,1,2) || '.' || substr(e.cnpj,3,3) || '.' || substr(e.cnpj,6,3) || '/' || substr(e.cnpj,9,4) || '-' || substr(e.cnpj,13,2) else e.cnpj end case, prod.nome,pp.quantidade, pp.valor_unitario,p.id_funcionario, fu.nome, p.id_fornecedor, f.nome  from pedidos p join fornecedores f on f.id_fornecedor = p.id_fornecedor join funcionarios fu on p.id_funcionario = fu.id_funcionario join estabelecimentos e on e.id_estabelecimento = p.id_estabelecimento join pedidos_produtos pp ON pp.id_pedido = p.id_pedido join produtos prod on prod.id_produto = pp.id_produto")
                query = cursor.fetchall()
                header = ['ID Pedido', 'Data do Pedido', 'ID Estabelecimento', 'CNPJ Estabelecimento', 'Nome do Produto', 'Quantidade', 'Valor Unitário', 'ID Funcionário', 'Nome Funcionário', 'ID Fornecedor', 'Nome Fornecedor']
                print(tabulate(query, headers=header))
            elif opcaoCRUD == 2:
                # Adicionar"
                data = datetime.now().strftime('%d/%m/%Y %H:%M')
                id_estabelecimento = input("Informe o ID do Estabelecimento: ")
                id_funcionario = input("Informe o ID do Funcionário: ")
                id_fornecedor = input("Informe o ID do Fornecedor: ")
                cursor.execute(
                    "INSERT INTO pedidos (data_pedido, id_estabelecimento, id_funcionario,id_fornecedor)  VALUES (%s, %s,%s,%s) RETURNING id_pedido;",
                    (data,id_estabelecimento, id_funcionario,id_fornecedor))
                conn.commit()
                id_pedido = cursor.fetchone()[0]
                insereProd=1
                while insereProd!=0:
                    id_produto = input("Informe o ID do Produto: ")
                    valor_un = input("Informe o valor unitário do produto: ")
                    qntd = input("Informe a quantidade de produtos comprados: ")
                    cursor.execute(
                        "INSERT INTO pedidos_produtos (quantidade, valor_unitario, id_produto,id_pedido)  VALUES (%s, %s,%s,%s);",
                        (qntd, valor_un, id_produto, id_pedido))
                    conn.commit()
                    insereProd=int(input("Deseja inserir mais um produto nesse pedido? 0 - Não, 1 - Sim "))
                    #Atualizar a quantidade de produtos na estabelecimentos_produtos e se não existir, cria um registro
            elif opcaoCRUD == 3:
                # Remover
                print("Remover")
                # Atualizar a quantidade de produtos na estabelecimentos_produtos
            elif opcaoCRUD == 4:
                # Editar
                print("Editar")
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))
    if opcao == 6:
        print("Vendas")

        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
                print("Mostrar todos")
            elif opcaoCRUD == 2:
                # Adicionar"
                print("Adicionar")
                # Atualizar a quantidade de produtos na estabelecimentos_produtos e se não existir produto o suficiente para venda, avisar na tela
            elif opcaoCRUD == 3:
                # Remover
                print("Remover")
                # Atualizar a quantidade de produtos na estabelecimentos_produtos
            elif opcaoCRUD == 4:
                # Editar
                print("Editar")
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))
    if opcao == 7:
        print("Relatórios")
        menuRelatorios()
        opcaoRel = int(input("Informe a opção: "))
        if opcaoRel == 1:
            #Produtos disponíveis em cada estabelecimento
            print("Produtos disponíveis em cada estabelecimento")
        elif opcaoRel ==2:
            #Vendas por funcionário
            print("Vendas por funcionário")
        elif opcaoRel == 3:
            #Compras por fornecedor
            print("Compras por fornecedor")
    menu()
    opcao = int(input("Digite sua opção: "))

 