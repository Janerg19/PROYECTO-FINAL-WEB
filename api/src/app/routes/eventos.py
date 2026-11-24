from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.eventos import EventosController
from app.middleware.auth import roles_required

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/eventos', methods=['GET'])
@jwt_required()
def listar_eventos():
    """Listar eventos"""
    return EventosController.listar_eventos()


@eventos_bp.route('/eventos', methods=['POST'])
@jwt_required()
@roles_required('docente', 'administrador')
def crear_evento():
    """Crear evento"""
    return EventosController.crear_evento()


@eventos_bp.route('/eventos/<int:evento_id>/participar', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente', 'administrador')
def participar_evento(evento_id):
    """Participar en evento"""
    return EventosController.participar_evento(evento_id)


@eventos_bp.route('/convocatorias', methods=['GET'])
@jwt_required()
def listar_convocatorias():
    """Listar convocatorias"""
    return EventosController.listar_convocatorias()


@eventos_bp.route('/convocatorias', methods=['POST'])
@jwt_required()
@roles_required('administrador')
def crear_convocatoria():
    """Crear convocatoria (solo admin)"""
    return EventosController.crear_convocatoria()


@eventos_bp.route('/convocatorias/<int:convocatoria_id>/validar', methods=['PATCH'])
@jwt_required()
@roles_required('administrador')
def validar_convocatoria(convocatoria_id):
    """Validar convocatoria (solo admin)"""
    return EventosController.validar_convocatoria(convocatoria_id)


@eventos_bp.route('/convocatorias/<int:convocatoria_id>/postular', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente')
def postular_convocatoria(convocatoria_id):
    """Postular a convocatoria"""
    return EventosController.postular_convocatoria(convocatoria_id)


@eventos_bp.route('/postulaciones', methods=['GET'])
@jwt_required()
@roles_required('administrador')
def listar_postulaciones():
    """Listar postulaciones (solo admin)"""
    return EventosController.listar_postulaciones()


@eventos_bp.route('/postulaciones/<int:postulacion_id>/resolver', methods=['PATCH'])
@jwt_required()
@roles_required('administrador')
def resolver_postulacion(postulacion_id):
    """Resolver postulación (solo admin)"""
    return EventosController.resolver_postulacion(postulacion_id)
