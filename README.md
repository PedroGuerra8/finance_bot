# 💰 Finance Bot — Controle Financeiro via Mensagens (API Backend)
linkedin.com/in/pedroguerra8

Projeto backend desenvolvido em Python com o objetivo de registrar e acompanhar movimentações financeiras através de mensagens em linguagem natural, simulando um assistente financeiro integrado ao WhatsApp.

O sistema interpreta textos enviados pelo usuário, classifica automaticamente a transação e mantém o controle atualizado do saldo.

---

## 🚀 Demonstração

Exemplos de comandos aceitos:
entrada 1500 salario
mercado 45,90
uber 18
saldo
total alimentação

O bot interpreta a mensagem, registra a transação e retorna o resultado automaticamente.

---

## 🧠 Funcionalidades

✅ Registro de entradas financeiras  
✅ Registro de saídas por categoria  
✅ Classificação automática de gastos  
✅ Cálculo automático de saldo  
✅ Consulta de totais por categoria  
✅ Parser de linguagem natural (Regex)  
✅ API REST pronta para integração com WhatsApp Cloud API  
✅ Persistência de dados com banco relacional

---

## 🏗️ Arquitetura do Projeto

O projeto foi estruturado seguindo separação em camadas para simular um backend real:

finance_bot/
│
├── controllers/ # Endpoints e rotas da API
├── services/ # Regras de negócio
├── models.py # Modelos do banco (ORM)
├── database.py # Configuração do banco SQLite
├── parser.py # Interpretação das mensagens
├── app.py # Inicialização da aplicação
└── requirements.txt


### Organização das responsabilidades

- **Controllers** → recebem requisições HTTP
- **Services** → executam regras de negócio
- **Models** → definem estrutura do banco
- **Parser** → interpreta mensagens do usuário

---

## ⚙️ Tecnologias Utilizadas

- Python
- Flask
- SQLAlchemy
- SQLite
- REST API
- Regex (processamento de texto)
- Ngrok (testes de webhook)

---

## 🗄️ Banco de Dados

O projeto utiliza **SQLite** com ORM via SQLAlchemy.

### Tabela principal: `transacoes`

| Campo | Descrição |
|------|-----------|
| id | Identificador da transação |
| tipo | Entrada ou saída |
| valor | Valor da movimentação |
| descricao | Descrição informada pelo usuário |
| data | Data do registro |

---

## ▶️ Como executar o projeto

```bash
# criar ambiente virtual
python -m venv venv

# ativar ambiente
venv\Scripts\activate

# instalar dependências
pip install -r requirements.txt

# executar aplicação
python app.py
