# Caminho do ambiente virtual e arquivos
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
ENV=.env

# Comando padrão
default: help

setup:
	@echo "[MAKE] Criando venv e instalando dependências..."
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

init-db:
	@echo "[MAKE] Verificando se o banco está acessível..."
	@if ! nc -z localhost 5432; then \
		echo "[MAKE] Banco não encontrado em localhost:5432. Subindo com Docker..."; \
		$(MAKE) start-db; \
		echo "[MAKE] Aguardando banco iniciar..."; \
		sleep 5; \
	fi

	@if [ ! -d "migrations" ]; then \
		echo "[MAKE] migrations/ não existe. Criando diretório vazio manualmente..."; \
		mkdir migrations; \
	fi

	@echo "[MAKE] Inicializando estrutura de migrações (se necessário)..."
	FLASK_APP=app.py $(PYTHON) -m flask db init || echo "[MAKE] Estrutura já existe."

	@echo "[MAKE] Gerando e aplicando migrações..."
	FLASK_APP=app.py $(PYTHON) -m flask db migrate -m "Initial migration" || echo "[MAKE] Nenhuma mudança detectada."
	FLASK_APP=app.py $(PYTHON) -m flask db upgrade

	@echo "[MAKE] Executando setup da aplicação (admin)..."
	$(PYTHON) -c "from website import create_app; from website.utils.setup import init_app; init_app(create_app())"

start-db:
	@echo "[MAKE] Iniciando container PostgreSQL..."
	docker run -d \
		--name seak_postgres \
		-e POSTGRES_USER=$$(grep DATABASE_USER $(ENV) | cut -d '=' -f2) \
		-e POSTGRES_PASSWORD=$$(grep DATABASE_PASSWORD $(ENV) | cut -d '=' -f2) \
		-e POSTGRES_DB=$$(grep PG_CHECK_DB $(ENV) | cut -d '=' -f2) \
		-v seak_data:/var/lib/postgresql/data \
		-p 5432:5432 \
		postgres:14

stop-db:
	@echo "[MAKE] Parando e removendo container..."
	-docker stop seak_postgres

destroy-db:
	@echo "[MAKE] Removendo container e volume..."
	-docker rm -f seak_postgres
	-docker volume rm seak_data

run:
	@echo "[MAKE] Executando o app com app.py"
	$(PYTHON) app.py

clean-db:
	rm -f instance/*.sqlite3

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup        → Cria o venv e instala dependências"
	@echo "  make start-db     → Sobe PostgreSQL com Docker"
	@echo "  make stop-db      → Para o container PostgreSQL"
	@echo "  make destroy-db   → Remove container + volume persistente"
	@echo "  make init-db      → Aplica migrações e cria admin"
	@echo "  make run          → Executa o app localmente com app.py"
	@echo "  make clean-db     → Remove banco SQLite local (se houver)"
