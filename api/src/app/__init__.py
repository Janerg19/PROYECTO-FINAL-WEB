from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, jwt, swagger
from utils.errors import register_error_handlers


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    CORS(app)
    
    # Registrar manejadores de error
    register_error_handlers(app)
    
    # Registrar blueprints
    from routes.usuarios import usuarios_bp
    from routes.investigacion import investigacion_bp
    from routes.eventos import eventos_bp
    from routes.comunidad import comunidad_bp
    from routes.gamificacion import gamificacion_bp
    
    app.register_blueprint(usuarios_bp, url_prefix='/api')
    app.register_blueprint(investigacion_bp, url_prefix='/api')
    app.register_blueprint(eventos_bp, url_prefix='/api')
    app.register_blueprint(comunidad_bp, url_prefix='/api')
    app.register_blueprint(gamificacion_bp, url_prefix='/api')
    
    # Configurar JWT
    app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = app.config['JWT_ACCESS_TOKEN_EXPIRES']
    
    # Configurar strict_slashes
    app.url_map.strict_slashes = False
    
    return app
