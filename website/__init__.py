import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuração principal
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-padrao-insegura')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Registro de Blueprints
    from .auth.routes import auth as auth_blueprint
    from .main.routes import main as main_blueprint
    from .admin.routes import admin as admin_blueprint
    from .list.routes import list_bp as list_blueprint
    from .search.routes import search as search_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(list_blueprint, url_prefix="/listar")
    app.register_blueprint(search_blueprint, url_prefix="/buscar")

    # Setup de banco de dados com proteção contra ambiente quebrado
    from website.utils.setup import init_app
    with app.app_context():
        try:
            init_app(app)
        except Exception as e:
            logging.warning(f"[INIT] Setup do banco falhou: {e}")

    return app
