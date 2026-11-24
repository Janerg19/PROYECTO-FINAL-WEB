from flask import request
from flask_jwt_extended import get_jwt_identity
from app.services.eventos import EventosService
from app.schemas.eventos import EventoCreateSchema, ConvocatoriaCreateSchema, PostulacionCreateSchema, PostulacionResolucionSchema
from app.utils.errors import ValidationError


class EventosController:
    """Controlador HTTP para eventos"""
    
    @staticmethod
    def listar_eventos():
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        eventos, total = EventosService.listar_eventos(limit, offset)
        from app.schemas.eventos import EventoSchema
        response_schema = EventoSchema(many=True)
        return {'eventos': response_schema.dump(eventos), 'total': total}, 200
    
    @staticmethod
    def crear_evento():
        creador_id = get_jwt_identity()
        schema = EventoCreateSchema()
        data = schema.load(request.json)
        evento = EventosService.crear_evento(data, creador_id)
        from app.schemas.eventos import EventoSchema
        response_schema = EventoSchema()
        return response_schema.dump(evento), 201
    
    @staticmethod
    def participar_evento(evento_id):
        usuario_id = get_jwt_identity()
        rol = request.json.get('rol', 'asistente')
        EventosService.participar_evento(evento_id, usuario_id, rol)
        return {'message': 'Participación registrada'}, 201
    
    @staticmethod
    def listar_convocatorias():
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        estado = request.args.get('estado')
        convocatorias, total = EventosService.listar_convocatorias(limit, offset, estado)
        from app.schemas.eventos import ConvocatoriaSchema
        response_schema = ConvocatoriaSchema(many=True)
        return {'convocatorias': response_schema.dump(convocatorias), 'total': total}, 200
    
    @staticmethod
    def crear_convocatoria():
        creador_id = get_jwt_identity()
        schema = ConvocatoriaCreateSchema()
        data = schema.load(request.json)
        convocatoria = EventosService.crear_convocatoria(data, creador_id)
        from app.schemas.eventos import ConvocatoriaSchema
        response_schema = ConvocatoriaSchema()
        return response_schema.dump(convocatoria), 201
    
    @staticmethod
    def validar_convocatoria(convocatoria_id):
        admin_id = get_jwt_identity()
        convocatoria = EventosService.validar_convocatoria(convocatoria_id, admin_id)
        from app.schemas.eventos import ConvocatoriaSchema
        response_schema = ConvocatoriaSchema()
        return response_schema.dump(convocatoria), 200
    
    @staticmethod
    def postular_convocatoria(convocatoria_id):
        usuario_id = get_jwt_identity()
        schema = PostulacionCreateSchema()
        data = schema.load(request.json)
        postulacion = EventosService.postular_convocatoria(convocatoria_id, data['propuesta'], usuario_id)
        from app.schemas.eventos import PostulacionConvocatoriaSchema
        response_schema = PostulacionConvocatoriaSchema()
        return response_schema.dump(postulacion), 201
    
    @staticmethod
    def listar_postulaciones():
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        postulaciones, total = EventosService.listar_postulaciones(limit, offset)
        from app.schemas.eventos import PostulacionConvocatoriaSchema
        response_schema = PostulacionConvocatoriaSchema(many=True)
        return {'postulaciones': response_schema.dump(postulaciones), 'total': total}, 200
    
    @staticmethod
    def resolver_postulacion(postulacion_id):
        admin_id = get_jwt_identity()
        schema = PostulacionResolucionSchema()
        data = schema.load(request.json)
        postulacion = EventosService.resolver_postulacion(postulacion_id, data['estado'], admin_id)
        from app.schemas.eventos import PostulacionConvocatoriaSchema
        response_schema = PostulacionConvocatoriaSchema()
        return response_schema.dump(postulacion), 200
