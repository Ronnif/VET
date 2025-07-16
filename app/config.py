"""
Configuración de la aplicación Flask para diferentes entornos (desarrollo, testing, producción).
Permite definir la clave secreta, la URI de la base de datos y otras opciones.
"""

from os import environ

class Config:
    # Clave secreta para sesiones y JWT
    SECRET_KEY = environ.get('SECRET_KEY', 'your_default_secret_key')
    # URI de la base de datos (por defecto, MySQL local)
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'mysql://user1:unknown1@localhost/veterinaria_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    # Configuración para desarrollo
    DEBUG = True

class TestingConfig(Config):
    # Configuración para testing (usa SQLite en memoria)
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    # Configuración para producción
    DEBUG = False

# Diccionario para seleccionar configuración según el entorno
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}