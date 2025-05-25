import os
import logging
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from flask_migrate import upgrade
from werkzeug.security import generate_password_hash
from website import db
from website.models import User

def init_app(app):
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            users_exists = inspector.has_table("users")
        except OperationalError as e:
            logging.error(f"[INIT] Erro ao inspecionar o banco: {e}")
            users_exists = False

        if not users_exists:
            logging.info("[INIT] Banco não inicializado. Aplicando migrações...")
            try:
                upgrade()
                logging.info("[INIT] Migrações aplicadas com sucesso.")
            except Exception as e:
                logging.error(f"[INIT] Falha ao aplicar migrações: {e}")
                return

        # Criar admin padrão
        admin_email = os.getenv("ADMIN_EMAIL", "admin@seak.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        admin_username = os.getenv("ADMIN_USERNAME", "Administrador Padrão")

        admin_exists = User.query.filter_by(is_default_admin=True).first()
        if not admin_exists:
            logging.info("[INIT] Criando usuário admin padrão...")
            admin = User(
                nome_usuario=admin_username,
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                is_default_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            logging.info("[INIT] Usuário admin criado com sucesso.")
        else:
            logging.info("[INIT] Usuário admin já existe.")
