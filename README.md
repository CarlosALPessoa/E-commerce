# E-commerce Books
📚 Livros e Microsserviços

Este projeto visa a estrutura de microsserviços para um website de catálogo de livros, desenvolvido com FastAPI, Flask, JS, HTML, Python e outras ferramentas. As aplicações usam uma estrutura simples e escalável para gerenciar registros de livros, usuários, carrinho, pedidos e configurações adicionais.

🛠️ Tecnologias Utilizadas

> Python — Linguagem principal usada em todos os microsserviços.

> Flask — Microframework usado no front.

> FastAPI — Framework moderno para APIs com Python.

> JWT(Json Web Token) — Autenticação e autorização.

> Uvicorn — Servidor ASGI rápido para FastAPI.

> Jinja2 — Template engine com Flask.

> SQLAlchemy — ORM para interação com banco de dados.

> SQLite — Banco de dados relacional leve, usado localmente durante o desenvolvimento.

📄 Descrição do Projeto

Este e-commerce conta com:
- Cadastro de livros;
- Listagem dos livros;
- Criação de usuários e atualização dos mesmos;
- Sistema de pagamento;
- Carrinho de pedidos;
- Pedidos.

A comunicação é feita via API REST.

🚀 Como Rodar o Projeto

Recomenda-se usar um ambiente virtual do python usando o python: `python3 -m venv .venv`

1. Clone o respositório.

2. Instale as dependências.
  Pré-requisitos:
  Execute o seguinte código na pasta em que encontram-se todos os microsserviços e que contenha o arquivo `requirements.txt`:
> pip install -r requirements.txt

3. Cada microsserviço precisará de um terminal específico. Podem ser inicializado seguindo os seguintes passos:

  a. User_auth e Front-end:

   Use um terminal para cada um dos microsserviços, entre na pasta `user_auth`, `frontend`, e execute: `python app.py`
   
  b. Para os outros serviços, em cada terminal, acesse as pastas: `payment`, `catalog`, `sale`, e execute: `python main.py` em cada terminal.

