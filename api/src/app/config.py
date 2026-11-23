import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'cambiar_esto_en_produccion')
    JWT_SECRET = os.getenv('JWT_SECRET', 'cambiar_esto_en_produccion')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))  # 24 horas en segundos
    
    # Base de datos PostgreSQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'riul')
    DB_USER = os.getenv('DB_USER', 'riul_app')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'cambiar_esto_en_produccion')
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False') == 'True'
    
    # Swagger
    SWAGGER_UI_JSON = '/api/openapi.json'
    SWAGGER_TEMPLATE = {
        "info": {
            "title": "RIUL API",
            "description": "API REST para Red de Investigación Universidad Libre",
            "version": "3.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT token en formato: Bearer {token}"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }


class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False


class TestingConfig(Config):
    """Configuración de pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://riul_app:test@localhost:5432/riul_test'


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
