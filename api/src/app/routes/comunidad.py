from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.comunidad import ComunidadController
from app.middleware.auth import roles_required

comunidad_bp = Blueprint('comunidad', __name__)

# Rutas de publicaciones
@comunidad_bp.route('/publicaciones', methods=['GET'])
@jwt_required()
def listar_publicaciones():
    """Listar publicaciones"""
    return ComunidadController.listar_publicaciones()


@comunidad_bp.route('/publicaciones', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente', 'administrador')
def crear_publicacion():
    """Crear publicación"""
    return ComunidadController.crear_publicacion()


@comunidad_bp.route('/publicaciones/<int:publicacion_id>', methods=['PUT'])
@jwt_required()
def actualizar_publicacion(publicacion_id):
    """Actualizar publicación (solo autor)"""
    return ComunidadController.actualizar_publicacion(publicacion_id)


@comunidad_bp.route('/publicaciones/<int:publicacion_id>', methods=['DELETE'])
@jwt_required()
def eliminar_publicacion(publicacion_id):
    """Eliminar publicación (solo autor)"""
    return ComunidadController.eliminar_publicacion(publicacion_id)


@comunidad_bp.route('/publicaciones/<int:publicacion_id>/comentarios', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente', 'administrador')
def crear_comentario(publicacion_id):
    """Crear comentario"""
    return ComunidadController.crear_comentario(publicacion_id)


@comunidad_bp.route('/publicaciones/<int:publicacion_id>/reacciones', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente', 'administrador')
def crear_reaccion(publicacion_id):
    """Crear reacción"""
    return ComunidadController.crear_reaccion(publicacion_id)


@comunidad_bp.route('/publicaciones/<int:publicacion_id>/reacciones', methods=['DELETE'])
@jwt_required()
@roles_required('estudiante', 'docente', 'administrador')
def quitar_reaccion(publicacion_id):
    """Quitar reacción"""
    return ComunidadController.quitar_reaccion(publicacion_id)


@comunidad_bp.route('/publicaciones/<int:publicacion_id>/compartir', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente', 'administrador')
def compartir_publicacion(publicacion_id):
    """Compartir publicación"""
    return ComunidadController.compartir_publicacion(publicacion_id)


# Rutas de notificaciones
@comunidad_bp.route('/notificaciones', methods=['GET'])
@jwt_required()
def listar_notificaciones():
    """Listar notificaciones"""
    return ComunidadController.listar_notificaciones()


@comunidad_bp.route('/notificaciones/<int:notificacion_id>', methods=['PATCH'])
@jwt_required()
def marcar_notificacion_leida(notificacion_id):
    """Marcar notificación como leída"""
    return ComunidadController.marcar_notificacion_leida(notificacion_id)
