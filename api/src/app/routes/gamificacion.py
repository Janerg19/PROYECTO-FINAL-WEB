from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.gamificacion import GamificacionController
from app.middleware.auth import roles_required

gamificacion_bp = Blueprint('gamificacion', __name__)

@gamificacion_bp.route('/gamificacion/me', methods=['GET'])
@jwt_required()
def obtener_gamificacion_me():
    """Obtener gamificación del usuario actual"""
    return GamificacionController.obtener_gamificacion_me()


@gamificacion_bp.route('/logros', methods=['GET'])
@jwt_required()
def listar_logros():
    """Listar logros del usuario"""
    return GamificacionController.listar_logros()


@gamificacion_bp.route('/logros', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente', 'administrador')
def enviar_logro():
    """Enviar logro para validación"""
    return GamificacionController.enviar_logro()


@gamificacion_bp.route('/logros/pendientes', methods=['GET'])
@jwt_required()
@roles_required('administrador')
def listar_logros_pendientes():
    """Listar logros pendientes (solo admin)"""
    return GamificacionController.listar_logros_pendientes()


@gamificacion_bp.route('/logros/<int:logro_id>/validar', methods=['PATCH'])
@jwt_required()
@roles_required('administrador')
def validar_logro(logro_id):
    """Validar logro (solo admin)"""
    return GamificacionController.validar_logro(logro_id)


@gamificacion_bp.route('/logros/<int:logro_id>/rechazar', methods=['PATCH'])
@jwt_required()
@roles_required('administrador')
def rechazar_logro(logro_id):
    """Rechazar logro (solo admin)"""
    return GamificacionController.rechazar_logro(logro_id)
