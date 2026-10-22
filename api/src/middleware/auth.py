import os
import jwt
from functools import wraps
from flask import request, jsonify, g

JWT_SECRET = os.getenv('JWT_SECRET', 'cambiar_esto_en_produccion')

def authenticate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token requerido'}), 401

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            g.user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 403

        return f(*args, **kwargs)
    return decorated_function

def require_role(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user'):
                return jsonify({'error': 'No autenticado'}), 401

            if g.user.get('rol') not in roles:
                return jsonify({'error': 'Rol no autorizado'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def optional_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if token:
            try:
                user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                g.user = user
            except:
                pass

        return f(*args, **kwargs)
    return decorated_function
