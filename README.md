# Projeto AvaliaUnB

O Projeto AvaliaUnB é uma aplicação web para avaliação de turmas e professores da Universidade de Brasília (UnB). Esta documentação fornece informações sobre como configurar e executar o projeto, bem como sobre os requisitos e funcionalidades principais.

## Requisitos

Certifique-se de ter os seguintes requisitos instalados em sua máquina antes de executar o projeto:

- Python (versão 3.6 ou superior)
- PostgreSQL (ou outro banco de dados compatível com psycopg2)
- Pacotes Python listados em `requirements.txt`

## Instalação

1. Clone o repositório do projeto para o seu ambiente local.
2. Crie um ambiente virtual para o projeto (recomendado, mas opcional).
3. Navegue até o diretório do projeto no terminal.
4. Execute o seguinte comando para instalar as dependências Python do projeto:

```
pip install -r requirements.txt
```

## Configuração do Banco de Dados

O projeto utiliza o PostgreSQL como banco de dados. Siga as etapas abaixo para configurar o banco de dados:

1. Certifique-se de ter o PostgreSQL instalado em sua máquina.
2. Crie um banco de dados no PostgreSQL para o projeto.
3. Defina as variáveis de ambiente necessárias para a conexão com o banco de dados. Crie um arquivo `.env` conforme o exemplo do documento .env.example na raiz do projeto e adicione as seguintes variáveis com seus respectivos valores:

```
DB_NAME=nomedobanco
DB_USER=usuariodobanco
DB_PASSWORD=senhadobanco
DB_HOST=localhose
DB_PORT=5432
```

Substitua `nomedobanco`, `usuariodobanco`, `senhadobanco`, `localhost` e `5432` pelos valores correspondentes às configurações do seu banco de dados PostgreSQL.

## Criação do Banco de Dados e Inserção de Dados

Antes de executar o projeto, é necessário criar as tabelas no banco de dados e inserir alguns dados iniciais. Siga as etapas abaixo:

1. Certifique-se de estar no diretório raiz do projeto.
2. Execute o seguinte comando para criar as tabelas no banco de dados, as views e as procedures:

```
python app.py
```

3. Abra um navegador da web e acesse `http://localhost:5000` para visualizar a aplicação.

## Utilização

A aplicação permite que os usuários façam login, registrem-se como novos usuários, visualizem turmas disponíveis, avaliem turmas e professores, denunciem avaliações e realizem outras ações relacionadas à avaliação acadêmica.

Acesse as diferentes rotas da aplicação para explorar as funcionalidades disponíveis. Por exemplo:

- `/login`: Página de login para usuários existentes.
- `/users/register`: Página de registro para novos usuários.
- `/turmas`: Página de visualização das turmas disponíveis.
- `/procedures/denuncias-nao-resolvidas`: Rota para obter a quantidade de denúncias não resolvidas.

