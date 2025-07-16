"""
Inicializa la aplicación Flask, las extensiones y registra los blueprints.
Configura la base de datos, migraciones, login y JWT.
"""

import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    """
    Crea y configura la aplicación Flask.
    - Carga la configuración según el entorno.
    - Inicializa las extensiones (DB, migraciones, login, JWT).
    - Registra los blueprints de rutas.
    - Crea las tablas automáticamente en desarrollo/testing.
    """
    app = Flask(__name__, instance_relative_config=True)
    from .config import config
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configura JWT usando la clave secreta
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    jwt = JWTManager(app)

    # Habilita CORS con soporte para credenciales
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Importa y registra blueprints de rutas principales
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Importa los modelos antes de crear las tablas
    from . import models  # Asegúrate de que los modelos estén importados
    # Crea tablas automáticamente solo en desarrollo o testing
    if app.config.get("DEBUG") or app.config.get("TESTING"):
        with app.app_context():
            db.create_all()

    @app.route('/', methods=['GET'])
    def index():
        return {"message": "API Backend de Veterinaria funcionando correctamente"}, 200

    return app