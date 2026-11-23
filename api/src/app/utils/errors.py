from flask import jsonify
from werkzeug.exceptions import HTTPException


class APIError(Exception):
    """Error base de la API"""
    def __init__(self, codigo, mensaje, detalles=None, status_code=400):
        self.codigo = codigo
        self.mensaje = mensaje
        self.detalles = detalles
        self.status_code = status_code
        super().__init__(mensaje)


class ValidationError(APIError):
    """Error de validación (400)"""
    def __init__(self, mensaje, detalles=None):
        super().__init__('VALIDATION_ERROR', mensaje, detalles, 400)


class AuthenticationError(APIError):
    """Error de autenticación (401)"""
    def __init__(self, mensaje='No autenticado'):
        super().__init__('AUTH_ERROR', mensaje, None, 401)


class AuthorizationError(APIError):
    """Error de autorización (403)"""
    def __init__(self, mensaje='No autorizado'):
        super().__init__('AUTHORIZATION_ERROR', mensaje, None, 403)


class NotFoundError(APIError):
    """Error de recurso no encontrado (404)"""
    def __init__(self, mensaje='Recurso no encontrado'):
        super().__init__('NOT_FOUND', mensaje, None, 404)


class ConflictError(APIError):
    """Error de conflicto (409)"""
    def __init__(self, mensaje, detalles=None):
        super().__init__('CONFLICT', mensaje, detalles, 409)


def register_error_handlers(app):
    """Registrar manejadores globales de errores"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = {
            'error': {
                'codigo': error.codigo,
                'mensaje': error.mensaje
            }
        }
        if error.detalles:
            response['error']['detalles'] = error.detalles
        return jsonify(response), error.status_code
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = {
            'error': {
                'codigo': 'HTTP_ERROR',
                'mensaje': error.description
            }
        }
        return jsonify(response), error.code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        app.logger.error(f"Error no manejado: {str(error)}")
        response = {
            'error': {
                'codigo': 'INTERNAL_ERROR',
                'mensaje': 'Error interno del servidor'
            }
        }
        return jsonify(response), 500
