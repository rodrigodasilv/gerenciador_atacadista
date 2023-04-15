import psycopg2
from tabulate import tabulate
import datetime


def menu():
    print("Informe a opção desejada:")
    print("1 - Estabelecimentos")
    print("2 - Funcionários")
    print("3 - Fornecedores")
    print("4 - Produtos")
    print("5 - Pedidos")
    print("6 - Relatórios")
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
                    "INSERT INTO estabelecimentos (telefone, cnpj) VALUES VALUES ('%s', '%s');",
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
            elif opcaoCRUD == 2:
                # Adicionar"
            elif opcaoCRUD == 3:
                # Remover
            elif opcaoCRUD == 4:
                # Editar
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))

    if opcao == 3:
        print("Fornecedores")

        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
            elif opcaoCRUD == 2:
                # Adicionar"
            elif opcaoCRUD == 3:
                # Remover
            elif opcaoCRUD == 4:
                # Editar
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))

    if opcao == 4:
        print("Produtos")
        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
            elif opcaoCRUD == 2:
                # Adicionar"
            elif opcaoCRUD == 3:
                # Remover
            elif opcaoCRUD == 4:
                # Editar
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))

    if opcao == 5:
        print("Pedidos")

        menuCRUD()
        opcaoCRUD = int(input("Informe a opção: "))
        while opcaoCRUD != 0:
            if opcaoCRUD == 1:
                # Mostrar todos
            elif opcaoCRUD == 2:
                # Adicionar"
            elif opcaoCRUD == 3:
                # Remover
            elif opcaoCRUD == 4:
                # Editar
            menuCRUD()
            opcaoCRUD = int(input("Informe a opção: "))
    if opcao == 6:
        print("Relatórios")
        menuRelatorios()
        opcaoRel = int(input("Informe a opção: "))
        if opcaoRel == 1:
            #Produtos disponíveis em cada estabelecimento
        elif opcaoRel ==2:
            #Vendas por funcionário
        elif opcaoRel == 3:
            #Compras por funcionário
    menu()
    opcao = int(input("Digite sua opção: "))

 