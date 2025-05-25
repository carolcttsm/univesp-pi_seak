# Projeto SEAK

Sistema Web para gestão de oficinas, turmas, alunos, professores e presenças.

---

## 🎯 Objetivo

Este sistema foi desenvolvido como solução para o Projeto Integrador III da UNIVESP. A proposta surgiu a partir da demanda de uma entidade assistencial (SEAK), que precisava de um controle mais eficiente para suas oficinas e alunos.

---

## 🚀 Deploy no Render

Este projeto está pronto para deploy no [Render](https://render.com).

### 📁 Estrutura esperada

- `app.py` (ponto de entrada)
- `Procfile` com:

```text
web: gunicorn app:app
```

### ⚙️ Variáveis de ambiente necessárias

- `DATABASE_URL` → URL completa do PostgreSQL
- `SECRET_KEY` → Chave de segurança Flask
- `ADMIN_EMAIL` *(opcional, padrão: admin@seak.com)*
- `ADMIN_PASSWORD` *(opcional, padrão: admin123)*
- `ADMIN_USERNAME` *(opcional, padrão: Administrador Padrão)*

### 🧱 Build e Start command

- **Build:** `pip install -r requirements.txt`
- **Start:** `gunicorn app:app`

---

## ✅ Comportamento no Primeiro Acesso

Se o banco estiver vazio, o sistema:

1. Aplica automaticamente as migrações
2. Cria um usuário administrador padrão

⚠️ **A recomendação é trocar a senha e/ou deletar esse admin após o primeiro login.**

---

## 💡 Tecnologias Utilizadas

- Python 3.11
- Flask 3.1.1
- PostgreSQL
- SQLAlchemy + Alembic
- Flask-Migrate, Flask-Login, Flask-WTF
- Render (deploy)
- Docker (uso local)

---

## 👥 Acesso de Teste

- **Email:** admin@seak.com  
- **Senha:** admin123

---

## 🪪 Licença

MIT — © SEAK 2025.  
Fotos utilizadas com permissão da instituição.

---

## 👨‍💻 Créditos

Grupo 009 — UNIVESP — SALA 001 — DRP10-PJI110
