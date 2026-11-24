from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.usuarios import UsuarioController
from app.middleware.auth import roles_required

usuarios_bp = Blueprint('usuarios', __name__)

# Rutas de autenticación
@usuarios_bp.route('/auth/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    return UsuarioController.register()


@usuarios_bp.route('/auth/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    return UsuarioController.login()


@usuarios_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def me():
    """Obtener usuario actual"""
    return UsuarioController.me()


# Rutas de usuarios (admin)
@usuarios_bp.route('/usuarios', methods=['GET'])
@jwt_required()
@roles_required('administrador')
def listar_usuarios():
    """Listar usuarios (solo admin)"""
    return UsuarioController.listar_usuarios()


@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
@jwt_required()
@roles_required('administrador')
def obtener_usuario(usuario_id):
    """Obtener usuario por ID (solo admin)"""
    return UsuarioController.obtener_usuario(usuario_id)


@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def actualizar_usuario(usuario_id):
    """Actualizar usuario (admin o propio usuario)"""
    return UsuarioController.actualizar_usuario(usuario_id)


@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
@roles_required('administrador')
def eliminar_usuario(usuario_id):
    """Eliminar usuario (solo admin)"""
    return UsuarioController.eliminar_usuario(usuario_id)


@usuarios_bp.route('/usuarios/<int:usuario_id>/aprobar', methods=['PATCH'])
@jwt_required()
@roles_required('administrador')
def aprobar_cuenta(usuario_id):
    """Aprobar cuenta de usuario (solo admin)"""
    return UsuarioController.aprobar_cuenta(usuario_id)


@usuarios_bp.route('/usuarios/<int:usuario_id>/rechazar', methods=['PATCH'])
@jwt_required()
@roles_required('administrador')
def rechazar_cuenta(usuario_id):
    """Rechazar cuenta de usuario (solo admin)"""
    return UsuarioController.rechazar_cuenta(usuario_id)


# Rutas de perfil
@usuarios_bp.route('/usuarios/<int:usuario_id>/perfil', methods=['PUT'])
@jwt_required()
def actualizar_perfil(usuario_id):
    """Actualizar perfil investigativo"""
    return UsuarioController.actualizar_perfil(usuario_id)
