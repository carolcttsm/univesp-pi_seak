# SEAK - Sistema de Gestão de Alunos e Oficinas

Este é um sistema web desenvolvido com Flask para gerenciar oficinas, turmas, alunos, professores e presenças, com autenticação e permissões de acesso administrativo.

---

## 🧪 Uso Local

Este projeto inclui um `Makefile` que automatiza o uso local com PostgreSQL via Docker.

### ⚙️ Pré-requisitos

- Python 3.11+
- Docker instalado
- Porta `5432` livre

### 🔧 Passo a passo

```bash
# 1. Clone o projeto
git clone https://github.com/seu-usuario/seak.git
cd seak

# 2. Copie o arquivo de ambiente
cp .env.example .env

# 3. Crie o ambiente virtual e instale dependências
make setup

# 4. Inicie o banco de dados via Docker
make start-db

# 5. Aplique migrações e crie o admin padrão (se necessário)
make init-db

# 6. Rode o app localmente
make run
```

Acesse em: [http://localhost:5000](http://localhost:5000)

---

## ✅ Usuário Admin Padrão

Ao iniciar pela primeira vez:

- **Email:** `admin@seak.com`
- **Senha:** `admin123`

⚠️ Após o login, cadastre um novo administrador e delete o padrão por segurança.

---

## 📦 Funcionalidades

### 👥 Alunos

- Cadastro, edição, exclusão
- Matrícula em turmas
- Registro de presenças
- Consulta de atividades por mês

### 👨‍🏫 Professores

- Cadastro, edição, exclusão
- Atribuição e visualização de oficinas e turmas

### 🏫 Oficinas

- Criação com número de vagas
- Listagem por mês
- Vínculo com turmas

### 📅 Turmas

- Cadastro e edição com dias/horários
- Alocação de alunos e professores

### ✅ Presenças

- Registro por data e oficina
- Consulta por aluno e mês

### 🔐 Autenticação

- Login de administradores
- Controle de acesso com Flask-Login

---

## 🗂️ Estrutura do Projeto

```
website/
├── admin/       # CRUD e controle de entidades
├── auth/        # Login e logout
├── list/        # Listagens
├── main/        # Entrada da aplicação
├── search/      # Filtros e buscas
├── static/      # Arquivos estáticos
├── templates/   # HTML com base nos blueprints
│   ├── add/
│   ├── edit/
│   ├── list/
│   ├── search/
│   ├── view/
│   └── base.html / home.html / admin-panel.html
├── forms.py     # Formulários WTForms
├── models.py    # Modelos SQLAlchemy
├── utils/       # Setup e inicialização do banco
│   └── setup.py
└── __init__.py  # Fábrica da aplicação Flask
```

---

## 🛠️ Makefile

Comandos disponíveis:

```bash
make setup        # Cria o venv e instala dependências
make start-db     # Sobe PostgreSQL com Docker
make stop-db      # Para o container
make destroy-db   # Remove container + volume
make init-db      # Aplica migrações e cria admin
make run          # Executa o app localmente
make clean-db     # Remove base SQLite (caso exista)
```

---

## 👥 Desenvolvido por

Grupo 009 — UNIVESP — DRP10-PJI110-SALA-001  
Fotos do SEAK utilizadas com permissão da instituição.
