from flask import request
from flask_jwt_extended import get_jwt_identity
from app.services.investigacion import InvestigacionService
from app.schemas.investigacion import (
    SemilleroSchema, SemilleroCreateSchema, SemilleroUpdateSchema,
    VinculacionSchema, VinculacionResolucionSchema,
    ProyectoSchema, ProyectoCreateSchema
)
from app.utils.errors import ValidationError


class InvestigacionController:
    """Controlador HTTP para investigación"""
    
    @staticmethod
    def listar_semilleros():
        """Listar semilleros"""
        try:
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            facultad_id = request.args.get('facultad_id', type=int)
            activo = request.args.get('activo', type=bool)
            
            semilleros, total = InvestigacionService.listar_semilleros(limit, offset, facultad_id, activo)
            
            response_schema = SemilleroSchema(many=True)
            return {
                'semilleros': response_schema.dump(semilleros),
                'total': total,
                'limit': limit,
                'offset': offset
            }, 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def obtener_semillero(semillero_id):
        """Obtener semillero por ID"""
        try:
            semillero = InvestigacionService.obtener_semillero(semillero_id)
            
            response_schema = SemilleroSchema()
            return response_schema.dump(semillero), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def crear_semillero():
        """Crear semillero (solo docente)"""
        try:
            creador_id = get_jwt_identity()
            
            schema = SemilleroCreateSchema()
            data = schema.load(request.json)
            
            semillero = InvestigacionService.crear_semillero(data, creador_id)
            
            response_schema = SemilleroSchema()
            return response_schema.dump(semillero), 201
            
        except Exception as e:
            raise e
    
    @staticmethod
    def actualizar_semillero(semillero_id):
        """Actualizar semillero (solo líder)"""
        try:
            solicitante_id = get_jwt_identity()
            
            schema = SemilleroUpdateSchema()
            data = schema.load(request.json)
            
            semillero = InvestigacionService.actualizar_semillero(semillero_id, data, solicitante_id)
            
            response_schema = SemilleroSchema()
            return response_schema.dump(semillero), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def solicitar_vinculacion(semillero_id):
        """Solicitar vinculación a semillero"""
        try:
            usuario_id = get_jwt_identity()
            
            data = {'semillero_id': semillero_id, 'usuario_id': usuario_id}
            vinculacion = InvestigacionService.solicitar_vinculacion(semillero_id, usuario_id)
            
            return {'message': 'Solicitud enviada', 'vinculacion_id': vinculacion.id}, 201
            
        except Exception as e:
            raise e
    
    @staticmethod
    def resolver_vinculacion(vinculacion_id):
        """Resolver solicitud de vinculación (solo líder)"""
        try:
            revisor_id = get_jwt_identity()
            
            schema = VinculacionResolucionSchema()
            data = schema.load(request.json)
            
            vinculacion = InvestigacionService.resolver_vinculacion(vinculacion_id, data['estado'], revisor_id)
            
            return {'message': f'Vinculación {data["estado"]}', 'vinculacion_id': vinculacion.id}, 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def listar_integrantes_semillero(semillero_id):
        """Listar integrantes de semillero"""
        try:
            integrantes = InvestigacionService.listar_integrantes_semillero(semillero_id)
            
            from app.schemas.investigacion import SemilleroIntegranteSchema
            response_schema = SemilleroIntegranteSchema(many=True)
            return response_schema.dump(integrantes), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def listar_proyectos():
        """Listar proyectos"""
        try:
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            semillero_id = request.args.get('semillero_id', type=int)
            estado = request.args.get('estado')
            
            proyectos, total = InvestigacionService.listar_proyectos(limit, offset, semillero_id, estado)
            
            response_schema = ProyectoSchema(many=True)
            return {
                'proyectos': response_schema.dump(proyectos),
                'total': total,
                'limit': limit,
                'offset': offset
            }, 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def crear_proyecto():
        """Crear proyecto (solo docente)"""
        try:
            creador_id = get_jwt_identity()
            
            schema = ProyectoCreateSchema()
            data = schema.load(request.json)
            
            proyecto = InvestigacionService.crear_proyecto(data, creador_id)
            
            response_schema = ProyectoSchema()
            return response_schema.dump(proyecto), 201
            
        except Exception as e:
            raise e
