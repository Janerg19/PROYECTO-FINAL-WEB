from flask import request
from flask_jwt_extended import get_jwt_identity
from app.services.comunidad import ComunidadService
from app.schemas.comunidad import (
    PublicacionSchema, PublicacionCreateSchema, PublicacionUpdateSchema,
    ComentarioCreateSchema, ReaccionCreateSchema, NotificacionUpdateSchema
)
from app.utils.errors import ValidationError


class ComunidadController:
    """Controlador HTTP para comunidad"""
    
    @staticmethod
    def listar_publicaciones():
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        categoria_id = request.args.get('categoria_id', type=int)
        usuario_id = request.args.get('usuario_id', type=int)
        publicaciones, total = ComunidadService.listar_publicaciones(limit, offset, categoria_id, usuario_id)
        response_schema = PublicacionSchema(many=True)
        return {
            'publicaciones': response_schema.dump(publicaciones),
            'total': total,
            'limit': limit,
            'offset': offset
        }, 200
    
    @staticmethod
    def crear_publicacion():
        creador_id = get_jwt_identity()
        schema = PublicacionCreateSchema()
        data = schema.load(request.json)
        publicacion = ComunidadService.crear_publicacion(data, creador_id)
        response_schema = PublicacionSchema()
        return response_schema.dump(publicacion), 201
    
    @staticmethod
    def actualizar_publicacion(publicacion_id):
        solicitante_id = get_jwt_identity()
        schema = PublicacionUpdateSchema()
        data = schema.load(request.json)
        publicacion = ComunidadService.actualizar_publicacion(publicacion_id, data, solicitante_id)
        response_schema = PublicacionSchema()
        return response_schema.dump(publicacion), 200
    
    @staticmethod
    def eliminar_publicacion(publicacion_id):
        solicitante_id = get_jwt_identity()
        ComunidadService.eliminar_publicacion(publicacion_id, solicitante_id)
        return {'message': 'Publicación eliminada'}, 200
    
    @staticmethod
    def crear_comentario(publicacion_id):
        usuario_id = get_jwt_identity()
        schema = ComentarioCreateSchema()
        data = schema.load(request.json)
        comentario = ComunidadService.crear_comentario(publicacion_id, data, usuario_id)
        return {'message': 'Comentario creado', 'comentario_id': comentario.id}, 201
    
    @staticmethod
    def crear_reaccion(publicacion_id):
        usuario_id = get_jwt_identity()
        schema = ReaccionCreateSchema()
        data = schema.load(request.json)
        reaccion = ComunidadService.crear_reaccion(publicacion_id, data['tipo'], usuario_id)
        return {'message': 'Reacción creada', 'reaccion_id': reaccion.id}, 201
    
    @staticmethod
    def quitar_reaccion(publicacion_id):
        usuario_id = get_jwt_identity()
        tipo = request.json.get('tipo')
        return ComunidadService.quitar_reaccion(publicacion_id, tipo, usuario_id), 200
    
    @staticmethod
    def compartir_publicacion(publicacion_id):
        usuario_id = get_jwt_identity()
        ComunidadService.compartir_publicacion(publicacion_id, usuario_id)
        return {'message': 'Publicación compartida'}, 201
    
    @staticmethod
    def listar_notificaciones():
        usuario_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        solo_no_leidas = request.args.get('solo_no_leidas', False, type=bool)
        notificaciones, total = ComunidadService.listar_notificaciones(usuario_id, limit, offset, solo_no_leidas)
        from app.schemas.comunidad import NotificacionSchema
        response_schema = NotificacionSchema(many=True)
        return {'notificaciones': response_schema.dump(notificaciones), 'total': total}, 200
    
    @staticmethod
    def marcar_notificacion_leida(notificacion_id):
        usuario_id = get_jwt_identity()
        schema = NotificacionUpdateSchema()
        data = schema.load(request.json)
        ComunidadService.marcar_notificacion_leida(notificacion_id, usuario_id)
        return {'message': 'Notificación marcada como leída'}, 200
