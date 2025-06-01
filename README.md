# 🏨 API de Cadastro de Hotéis em Python

Bem-vindo(a) ao repositório da API de Cadastro de Hotéis! Este projeto consiste em uma API RESTful desenvolvida em Python, projetada para gerenciar informações de hotéis,
como nome, estrelas, diária e cidade. É uma aplicação robusta e escalável,ideal para servir como backend para sistemas de reserva ou consulta de hotéis.

## 🚀 Sobre o Projeto

Este projeto demonstra a criação de uma API em Python, cobrindo desde a configuração do ambiente até a persistência de dados e a exposição de endpoints REST. O objetivo é fornecer uma base sólida para o desenvolvimento de APIs backend, utilizando as melhores práticas da linguagem e ferramentas modernas.

## 🗺️ Endpoints da API

### Hoteis

* 🔍 `GET /hoteis` - Retorna uma lista de todos os hotéis cadastrados.
* 🔍 `GET /hoteis/{hotel_id}` - Retorna os detalhes de um hotel específico.
* 📝 `POST /hoteis` - Cria um novo cadastro de hotel.
* 🔄 `PUT /hoteis/{hotel_id}` - Atualiza os dados de um hotel existente.
* ❌ `DELETE /hoteis/{hotel_id}` - Remove um hotel do cadastro.

### Users

* 🔍 `GET /users/{user_id}` - Retorna o ID do usuário e o login.
* 📝 `POST /register` - Cria um novo cadastro de usuário.
* ❌ `DELETE /users/{hotel_id}` - Remove um usuário.

## ⚙️ Como Rodar o Projeto (Configuração Local)

Siga os passos abaixo para configurar e executar a API em seu ambiente local:

### Pré-requisitos
* **Python 3.x**
* **Pip** (gerenciador de pacotes do Python)

### 1. Clonar o Repositório
git clone (https://github.com/Djeferson-Almeida/Python-Rest-Api)

### 2. Instalar as dependências
* `pip install Flask`
* `pip install flask_restful`
* `pip install SQLAlchemy`
*
## 🛠️ Tecnologias Utilizadas
Este projeto foi desenvolvido utilizando as seguintes tecnologias e ferramentas:

* **Python** 
* **Flask** 
* **Flask-RESTful**
* **VS Code** 
* **Git / GitHub**
* **Postman**
