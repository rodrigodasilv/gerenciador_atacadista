
# Funções gerais
# Alunos: Guilherme Alves && Rodrigo da Silva

import pyodbc
import os
from utilities import *
from tabulate import tabulate

driver='PostgreSQL ANSI(x64)'
host='127.0.0.1'
port='5432'
dbname='db_atacadista'
user='postgres'
password='123'

# Driver MySQL ODBC 8.0 ANSI Driver
# MariaDB -> root / secret

def pause():
    os.system("pause")
def clear():
    os.system("cls")
def break_line():
    print('\n')

def int_input(texto):
    num = int(input(texto))
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

def menuTabelas(): # Apenas das tabelas entidade
    clear()
    print("Informe a opção desejada:")
    print("1 - Estabelecimentos")
    print("2 - Funcionários")
    print("3 - Fornecedores")
    print("4 - Produtos")
    print("0 - Voltar")

    break_line()
    escolha = int_input("Informe a opção: ")
    return escolha

def menuRelatorios():
    clear()
    print("Informe o relatório desejado:")
    print("1 - Produtos disponíveis em cada estabelecimento")
    print("2 - Vendas por funcionário")
    print("3 - Compras por funcionário")
    print("0 - Voltar")

    break_line()
    escolha = int_input("Informe a opção: ")
    return escolha

def connect_banco():
    return pyodbc.connect('DRIVER={' + driver + '};SERVER='+host+';PORT=' + port + ';DATABASE='+dbname+';UID=' + user + ';PWD=' + password + ';', autocommit=False)

def cursor_banco():
    return connect_banco().cursor()

def query_banco(query):
    with cursor_banco() as cursor:
        if 'SELECT' in query.upper():
            return cursor.execute(query).fetchall() 
        else:
            cursor.execute(query) # Aparentemente não precisa fazer cursor().commit()
            print("Query executada.")

def print_tabulado(query, header):
    print(tabulate(query, headers=header))
    
def solicitar_inputs(persona, *inputs):
    lista_inputs = []
    for _input in inputs:
        entrada = None
        if _input == 'chave':
            entrada = int_input(f'Digite o ID do {persona}: ')
            if entrada <= 0:
                entrada = None
                print('ID invalido!')
        if _input == 'cnpj':
            entrada = input(f'Informe o CNPJ do {persona}: ')
            #if not valida_cnpj(entrada):
            #    print('CNPJ invalido!')
            #    entrada = None
        if _input == 'cpf':
            entrada = input(f'Informe o CPF do {persona}: ')
            #if not valida_cpf(entrada):
            #   print('CPF invalido!')
            #    entrada = None
        if _input == 'descricao':
            entrada = input(f"Informe a descricao do {persona}: ")
        if _input == 'email':
            entrada = input(f'Informe o E-mail do {persona}: ')
            if not valida_email(entrada):
                print('E-mail invalido!')
                entrada = None
        if _input == 'nome':
            entrada = input(f'Informe o Nome completo do {persona}: ')
        if _input == 'telefone':
            entrada = input(f'Informe o telefone do {persona} (com DDD): ')
        if entrada:
            lista_inputs.append(entrada)

    return lista_inputs

def valida_cnpj(cnpj):
    cnpj = str(cnpj)
    # Remove caracteres não numéricos, como traços e pontos
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verifica se o CNPJ possui 14 dígitos
    if len(cnpj) != 14:
        return False

    # Algoritmo de validação de CNPJ por digito verificador
    digito_verificador = [0, 0]
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for index, digito in enumerate(cnpj[:12]):
        soma += int(digito) * pesos[index]
    num = soma % 11
    if num < 2:
        digito_verificador[0] = 0
    else:
        digito_verificador[0] = 11 - num

    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for index, digito in enumerate(cnpj[:12] + str(digito_verificador[0])):
        soma += int(digito) * pesos[index]
    num = soma % 11
    if num < 2:
        digito_verificador[1] = 0
    else:
        digito_verificador[1] = 11 - num
    
    if digito_verificador[0] == int(cnpj[12]) and digito_verificador[1] == int(cnpj[13]):
        return True
    return False

def valida_cpf(cpf):
    cpf = str(cpf)
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    peso = 10
    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1
    digito1 = (11 - soma % 11) if soma % 11 >= 2 else 0

    # Calcula o segundo dígito verificador
    soma = 0
    peso = 11
    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1
    digito2 = (11 - soma % 11) if soma % 11 >= 2 else 0

    # Verifica se os dígitos verificadores calculados são iguais aos fornecidos no CPF
    if int(cpf[9]) == digito1 and int(cpf[10]) == digito2:
        return True
    else:
        return False

def valida_email(email):
    if email.count("@") == 1 and "." in email.split("@")[1]:
        if not email.startswith(".") and not email.endswith("."):
            if not email.split("@")[0].endswith('.') and not email.split("@")[1].startswith('.'):
                return True
    
    return False
