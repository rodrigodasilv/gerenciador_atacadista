# Gerenciador atacadista

### Introdução

O domínio escolhido para o trabalho de BAN2 foi um mercado atacadista, possuindo várias instalações em diferentes localidades e necessitando gerenciar entradas e saídas de produtos, vinculando-os com seus respectivos funcionários, fornecedores e estabelecimentos. 

### Requisitos

1 - PostgreSQL

2 - Python > 3.6

### Instalação

#### Banco de dados

1 - Abrir o pgAdmin.

![image](https://user-images.githubusercontent.com/84868817/232265227-1d8e4ff5-8710-46f0-b8a4-2df925ef4c82.png)

2 - Clique com o botão direito em Databases e clique em `Create > Database`.

![image](https://user-images.githubusercontent.com/84868817/232265482-0a614fc5-9d37-4c4f-84ab-6b98eb678ab3.png)

3 - Nomeie o banco como `db_atacadista` e clique em `Save`.

![image](https://user-images.githubusercontent.com/84868817/232265494-81ae5546-f7c7-41c0-8f8a-886c5de4ffbc.png)

4 - Clique com o botão direito no banco criado, e clique em `Query Tool`.

![image](https://user-images.githubusercontent.com/84868817/232265523-4dc52fe7-3524-46e0-8b0a-78011edd747d.png)

5 - Executar a query disponível no repositório como `db_atacadista.sql`.

![image](https://user-images.githubusercontent.com/84868817/232265841-fbc5f35b-a255-461b-8cd8-d5e79a253623.png)

#### Python

Instalar o Python, com a opção `Add python.exe to PATH` selecionada:

![image](https://user-images.githubusercontent.com/84868817/232258651-c949e3c9-5566-411b-b144-e06e2fd7dd65.png)

### Tutorial

Abrir o CMD e utilizar o comando `cd` para alterar o diretório para a pasta que o repositório foi baixado. Após isso, utilizar o comando `pip install -r requirements.txt` para instalar as dependências do Python:

![image](https://user-images.githubusercontent.com/55567123/232244195-4b2d33c9-cf56-45df-8e41-4aa95119a8fd.png)

Após a instalação das dependências, utilizar o comando `python main.py` para executar o programa:

![image](https://user-images.githubusercontent.com/55567123/232244620-b77711c7-81e7-44d7-ac7a-38432757e171.png)
