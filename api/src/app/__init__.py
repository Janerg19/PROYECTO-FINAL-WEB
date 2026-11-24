from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from app.config import Config
from app.extensions import db, jwt
from app.utils.errors import register_error_handlers


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Configurar Swagger/OpenAPI
    swagger_template = {
        "info": {
            "title": "RIUL API",
            "description": "API REST para Red de Investigación Universidad Libre",
            "version": "3.0",
            "contact": {
                "name": "Universidad Libre"
            }
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
    swagger = Swagger(template=swagger_template)
    swagger.init_app(app)
    
    # Registrar manejadores de error
    register_error_handlers(app)
    
    # Registrar blueprints
    from app.routes.usuarios import usuarios_bp
    from app.routes.investigacion import investigacion_bp
    from app.routes.eventos import eventos_bp
    from app.routes.comunidad import comunidad_bp
    from app.routes.gamificacion import gamificacion_bp
    
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
    
    # Endpoint de health check
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'API RIUL funcionando'}, 200
    
    return app
