from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.investigacion import InvestigacionController
from app.middleware.auth import roles_required

investigacion_bp = Blueprint('investigacion', __name__)

# Rutas de semilleros
@investigacion_bp.route('/semilleros', methods=['GET'])
@jwt_required()
def listar_semilleros():
    """Listar semilleros"""
    return InvestigacionController.listar_semilleros()


@investigacion_bp.route('/semilleros/<int:semillero_id>', methods=['GET'])
@jwt_required()
def obtener_semillero(semillero_id):
    """Obtener semillero por ID"""
    return InvestigacionController.obtener_semillero(semillero_id)


@investigacion_bp.route('/semilleros', methods=['POST'])
@jwt_required()
@roles_required('docente', 'administrador')
def crear_semillero():
    """Crear semillero (solo docente)"""
    return InvestigacionController.crear_semillero()


@investigacion_bp.route('/semilleros/<int:semillero_id>', methods=['PUT'])
@jwt_required()
def actualizar_semillero(semillero_id):
    """Actualizar semillero (solo líder)"""
    return InvestigacionController.actualizar_semillero(semillero_id)


@investigacion_bp.route('/semilleros/<int:semillero_id>/solicitar', methods=['POST'])
@jwt_required()
@roles_required('estudiante', 'docente')
def solicitar_vinculacion(semillero_id):
    """Solicitar vinculación a semillero"""
    return InvestigacionController.solicitar_vinculacion(semillero_id)


@investigacion_bp.route('/semilleros/<int:semillero_id>/integrantes', methods=['GET'])
@jwt_required()
def listar_integrantes_semillero(semillero_id):
    """Listar integrantes de semillero"""
    return InvestigacionController.listar_integrantes_semillero(semillero_id)


@investigacion_bp.route('/vinculaciones/<int:vinculacion_id>/resolver', methods=['PATCH'])
@jwt_required()
@roles_required('docente', 'administrador')
def resolver_vinculacion(vinculacion_id):
    """Resolver solicitud de vinculación (solo líder del semillero)"""
    return InvestigacionController.resolver_vinculacion(vinculacion_id)


# Rutas de proyectos
@investigacion_bp.route('/proyectos', methods=['GET'])
@jwt_required()
def listar_proyectos():
    """Listar proyectos"""
    return InvestigacionController.listar_proyectos()


@investigacion_bp.route('/proyectos', methods=['POST'])
@jwt_required()
@roles_required('docente', 'administrador')
def crear_proyecto():
    """Crear proyecto (solo docente)"""
    return InvestigacionController.crear_proyecto()
