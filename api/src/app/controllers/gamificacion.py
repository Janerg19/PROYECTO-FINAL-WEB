from flask import request
from flask_jwt_extended import get_jwt_identity
from app.services.gamificacion import GamificacionService
from app.schemas.gamificacion import LogroCreateSchema, LogroResolucionSchema
from app.utils.errors import ValidationError


class GamificacionController:
    """Controlador HTTP para gamificación"""
    
    @staticmethod
    def obtener_gamificacion_me():
        usuario_id = get_jwt_identity()
        gamificacion = GamificacionService.obtener_gamificacion_usuario(usuario_id)
        return gamificacion, 200
    
    @staticmethod
    def listar_logros():
        usuario_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        estado = request.args.get('estado')
        logros, total = GamificacionService.listar_logros(usuario_id, limit, offset, estado)
        from app.schemas.gamificacion import LogroSchema
        response_schema = LogroSchema(many=True)
        return {'logros': response_schema.dump(logros), 'total': total}, 200
    
    @staticmethod
    def listar_logros_pendientes():
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        logros, total = GamificacionService.listar_logros_pendientes(limit, offset)
        from app.schemas.gamificacion import LogroSchema
        response_schema = LogroSchema(many=True)
        return {'logros': response_schema.dump(logros), 'total': total}, 200
    
    @staticmethod
    def enviar_logro():
        usuario_id = get_jwt_identity()
        schema = LogroCreateSchema()
        data = schema.load(request.json)
        logro = GamificacionService.enviar_logro(data, usuario_id)
        from app.schemas.gamificacion import LogroSchema
        response_schema = LogroSchema()
        return response_schema.dump(logro), 201
    
    @staticmethod
    def validar_logro(logro_id):
        admin_id = get_jwt_identity()
        logro = GamificacionService.validar_logro(logro_id, admin_id)
        from app.schemas.gamificacion import LogroSchema
        response_schema = LogroSchema()
        return response_schema.dump(logro), 200
    
    @staticmethod
    def rechazar_logro(logro_id):
        admin_id = get_jwt_identity()
        logro = GamificacionService.rechazar_logro(logro_id, admin_id)
        from app.schemas.gamificacion import LogroSchema
        response_schema = LogroSchema()
        return response_schema.dump(logro), 200
