
# Funções gerais
# Alunos: Guilherme Alves && Rodrigo da Silva

import psycopg2
import os
from utilities import *
from tabulate import tabulate

dbname='db_atacadista'
user='postgres'
password='admin'

def pause():
    os.system("pause")
def clear():
    os.system("cls")
def break_line():
    print('\n')

def print_pause(texto):
    print(texto)
    pause()

def int_input(texto):
    num = input(texto)
    if num.isnumeric():
        num = int(num)
    else:
        num = None
    return num

def menuInicial():
    clear()
    print("Informe a opção desejada:")
    print("1 - Cadastro")
    print("2 - Consulta")
    print("3 - Atualização")
    print("4 - Remoção")
    print("5 - Registrar venda")
    print("6 - Realizar pedido")
    print("7 - Relatórios")
    print("0 - Sair")
    
    break_line()

    escolha = int_input("Informe a opção: ")
    return escolha

def menuTabelas(temTabelasEntidade = False): # Apenas das tabelas entidade
    clear()
    print("Informe a opção desejada:")
    print("1 - Estabelecimentos")
    print("2 - Funcionários")
    print("3 - Fornecedores")
    print("4 - Produtos")
    print("5 - Pedidos")
    print("6 - Vendas")

    if temTabelasEntidade:
        print("7 - Produtos dos pedidos")
        print("8 - Produtos das vendas")

    print("0 - Voltar")

    break_line()
    escolha = int_input("Informe a opção: ")
    return escolha

def menuRelatorios():
    clear()
    print("Informe o relatório desejado:")
    print("1 - Produtos disponíveis em cada estabelecimento")
    print("2 - Vendas por funcionário")
    print("3 - Compras por fornecedor")
    print("0 - Voltar")

    break_line()
    escolha = int_input("Informe a opção: ")
    return escolha

def connect_banco():
    con = psycopg2.connect(f"dbname={dbname} user={user} password={password}")
    con.autocommit = True
    return con

def cursor_banco():
    return connect_banco().cursor()

def query_banco(query):
    with cursor_banco() as cursor:
        if 'SELECT' in query.upper():
            cursor.execute(query)
            return cursor.fetchall() 
        else:
            cursor.execute(query) 
            print("Query executada.")
            print(query)

def print_tabulado(query, header):
    print(tabulate(query, headers=header))
    
def solicitar_inputs(persona, *inputs):
    lista_inputs = []
    for _input in inputs:
        entrada = None
        if _input == 'chave':
            entrada = int_input(f'Digite o ID do {persona}: ')
            if entrada and entrada <= 0:
                print('ID invalido!')
                entrada = None
        if _input == 'cnpj':
            entrada = input(f'Informe o CNPJ do {persona}: ')
            if not valida_cnpj(entrada):
                print('CNPJ invalido!')
                entrada = None
        if _input == 'cpf':
            entrada = input(f'Informe o CPF do {persona}: ')
            if not valida_cpf(entrada):
                print('CPF invalido!')
                entrada = None
        if _input == 'descricao':
            entrada = input(f"Informe a descricao do {persona}: ")
        if _input == 'email':
            entrada = input(f'Informe o E-mail do {persona}: ')
            if not valida_email(entrada):
                print('E-mail invalido!')
                entrada = None
        if _input == 'nome':
            entrada = input(f'Informe o Nome completo do {persona}: ')
            if entrada.isnumeric():
                print('Nome invalido!')
                entrada = None
        if _input == 'telefone':
            entrada = input(f'Informe o telefone do {persona} (com DDD): ')
        
        lista_inputs.append(entrada)

    if len(lista_inputs) == 1:
        return lista_inputs[0]

    return lista_inputs

def valida_cnpj(cnpj):
    cnpj = str(cnpj)
    cnpj = ''.join(filter(str.isdigit, cnpj)) # Remove caracteres não numéricos, como traços e pontos

    # Verifica se o CNPJ possui 14 dígitos
    if len(cnpj) != 14:
        return False
    return True

def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = ''.join(filter(str.isdigit, cpf)) # Remove caracteres não numéricos

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False
    return True

def valida_email(email):
    if email.count("@") == 1 and "." in email.split("@")[1]:
        if not email.startswith(".") and not email.endswith("."):
            if not email.split("@")[0].endswith('.') and not email.split("@")[1].startswith('.'):
                return True
    
    return False
