from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from utils.errors import AuthorizationError, AuthenticationError


def roles_required(*roles):
    """Decorador para verificar que el usuario tenga al menos uno de los roles requeridos"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            verify_jwt_in_request()
            
            # Obtener el token actual
            user_id = get_jwt_identity()
            token_data = get_jwt()
            
            # Verificar que el rol del usuario esté en la lista de roles permitidos
            user_role = token_data.get('rol')
            if user_role not in roles:
                raise AuthorizationError(f'Se requiere uno de los siguientes roles: {", ".join(roles)}')
            
            return f(*args, **kwargs)
        return wrapped
    return decorator


def optional_auth(f):
    """Decorador para autenticación opcional (permitir acceso a visitantes)"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            pass  # Si no hay token, continuar sin autenticación
        return f(*args, **kwargs)
    return wrapped


def get_current_user():
    """Obtener el usuario actual desde el JWT"""
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception:
        return None


def get_current_role():
    """Obtener el rol del usuario actual desde el JWT"""
    try:
        verify_jwt_in_request()
        token_data = get_jwt()
        return token_data.get('rol')
    except Exception:
        return None
