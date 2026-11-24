from datetime import datetime
from app.extensions import db
from app.models.comunidad import (
    Publicacion, Comentario, Reaccion, Compartido,
    SeguimientoUsuario, SeguimientoSemillero, Notificacion,
    CategoriaPublicacion, Evidencia, PublicacionEvidencia
)
from app.models.gamificacion import TipoActividadXP, MovimientoXP
from app.models.usuarios import Usuario
from app.utils.errors import ValidationError, NotFoundError, ConflictError


class ComunidadService:
    """Servicio de lógica de negocio para comunidad"""
    
    @staticmethod
    def listar_publicaciones(limit=50, offset=0, categoria_id=None, usuario_id=None):
        """Listar publicaciones con filtros"""
        query = Publicacion.query.filter(Publicacion.eliminado_en.is_(None))
        
        if categoria_id:
            query = query.filter(Publicacion.categoria_id == categoria_id)
        
        if usuario_id:
            query = query.filter(Publicacion.usuario_id == usuario_id)
        
        publicaciones = query.order_by(Publicacion.creado_en.desc()).limit(limit).offset(offset).all()
        total = query.count()
        
        return publicaciones, total
    
    @staticmethod
    def crear_publicacion(data, creador_id):
        """Crear publicación"""
        publicacion = Publicacion(
            categoria_id=data['categoria_id'],
            usuario_id=creador_id,
            semillero_id=data.get('semillero_id'),
            titulo=data['titulo'],
            contenido=data['contenido']
        )
        
        db.session.add(publicacion)
        db.session.flush()
        
        # Otorgar XP por publicación
        ComunidadService._otorgar_xp(creador_id, 'publicacion', referencia_id=publicacion.id)
        
        # Crear notificación a seguidores (simplificado)
        # ComunidadService._notificar_seguidores(creador_id, 'publicacion', publicacion.id)
        
        db.session.commit()
        
        return publicacion
    
    @staticmethod
    def actualizar_publicacion(publicacion_id, data, solicitante_id):
        """Actualizar publicación (solo autor)"""
        publicacion = Publicacion.query.get(publicacion_id)
        if not publicacion:
            raise NotFoundError('Publicación no encontrada')
        
        if publicacion.usuario_id != solicitante_id:
            raise ValidationError('Solo el autor puede actualizar la publicación')
        
        if 'titulo' in data:
            publicacion.titulo = data['titulo']
        if 'contenido' in data:
            publicacion.contenido = data['contenido']
        if 'categoria_id' in data:
            publicacion.categoria_id = data['categoria_id']
        
        publicacion.actualizado_en = datetime.utcnow()
        db.session.commit()
        
        return publicacion
    
    @staticmethod
    def eliminar_publicacion(publicacion_id, solicitante_id):
        """Borrado lógico de publicación (solo autor)"""
        publicacion = Publicacion.query.get(publicacion_id)
        if not publicacion:
            raise NotFoundError('Publicación no encontrada')
        
        if publicacion.usuario_id != solicitante_id:
            raise ValidationError('Solo el autor puede eliminar la publicación')
        
        publicacion.eliminado_en = datetime.utcnow()
        db.session.commit()
        
        return publicacion
    
    @staticmethod
    def crear_comentario(publicacion_id, data, usuario_id):
        """Crear comentario en publicación"""
        comentario = Comentario(
            publicacion_id=publicacion_id,
            usuario_id=usuario_id,
            contenido=data['contenido']
        )
        
        db.session.add(comentario)
        db.session.flush()
        
        # Otorgar XP por comentario
        ComunidadService._otorgar_xp(usuario_id, 'comentario', referencia_id=comentario.id)
        
        # Notificar al autor de la publicación
        publicacion = Publicacion.query.get(publicacion_id)
        if publicacion.usuario_id != usuario_id:
            ComunidadService._crear_notificacion(
                publicacion.usuario_id,
                'comentario',
                f'{Usuario.query.get(usuario_id).nombres} comentó tu publicación',
                referencia_tipo='comentario',
                referencia_id=comentario.id
            )
        
        db.session.commit()
        
        return comentario
    
    @staticmethod
    def crear_reaccion(publicacion_id, tipo, usuario_id):
        """Crear reacción a publicación"""
        # Verificar si ya existe reacción del mismo tipo
        existente = Reaccion.query.filter_by(
            publicacion_id=publicacion_id,
            usuario_id=usuario_id,
            tipo=tipo
        ).first()
        
        if existente:
            raise ConflictError('Ya tienes esta reacción en esta publicación')
        
        reaccion = Reaccion(
            publicacion_id=publicacion_id,
            usuario_id=usuario_id,
            tipo=tipo
        )
        
        db.session.add(reaccion)
        db.session.flush()
        
        # Otorgar XP por reacción (solo si es primera reacción a esta publicación)
        reacciones_usuario = Reaccion.query.filter_by(
            publicacion_id=publicacion_id,
            usuario_id=usuario_id
        ).count()
        
        if reacciones_usuario == 1:
            ComunidadService._otorgar_xp(usuario_id, 'reaccion', referencia_id=reaccion.id)
        
        # Notificar al autor
        publicacion = Publicacion.query.get(publicacion_id)
        if publicacion.usuario_id != usuario_id:
            ComunidadService._crear_notificacion(
                publicacion.usuario_id,
                'reaccion',
                f'{Usuario.query.get(usuario_id).nombres} reaccionó a tu publicación',
                referencia_tipo='reaccion',
                referencia_id=reaccion.id
            )
        
        db.session.commit()
        
        return reaccion
    
    @staticmethod
    def quitar_reaccion(publicacion_id, tipo, usuario_id):
        """Quitar reacción"""
        reaccion = Reaccion.query.filter_by(
            publicacion_id=publicacion_id,
            usuario_id=usuario_id,
            tipo=tipo
        ).first()
        
        if not reaccion:
            raise NotFoundError('Reacción no encontrada')
        
        db.session.delete(reaccion)
        db.session.commit()
        
        return {'message': 'Reacción eliminada'}
    
    @staticmethod
    def compartir_publicacion(publicacion_id, usuario_id):
        """Compartir publicación"""
        existente = Compartido.query.filter_by(
            publicacion_id=publicacion_id,
            usuario_id=usuario_id
        ).first()
        
        if existente:
            raise ConflictError('Ya compartiste esta publicación')
        
        compartido = Compartido(
            publicacion_id=publicacion_id,
            usuario_id=usuario_id
        )
        
        db.session.add(compartido)
        db.session.commit()
        
        return compartido
    
    @staticmethod
    def seguir_usuario(seguido_id, seguidor_id):
        """Seguir a un usuario"""
        if seguidor_id == seguido_id:
            raise ValidationError('No puedes seguirte a ti mismo')
        
        existente = SeguimientoUsuario.query.filter_by(
            seguidor_id=seguidor_id,
            seguido_id=seguido_id
        ).first()
        
        if existente:
            raise ConflictError('Ya sigues a este usuario')
        
        seguimiento = SeguimientoUsuario(
            seguidor_id=seguidor_id,
            seguido_id=seguido_id
        )
        
        db.session.add(seguimiento)
        db.session.commit()
        
        return seguimiento
    
    @staticmethod
    def dejar_de_seguir_usuario(seguido_id, seguidor_id):
        """Dejar de seguir a un usuario"""
        seguimiento = SeguimientoUsuario.query.filter_by(
            seguidor_id=seguidor_id,
            seguido_id=seguido_id
        ).first()
        
        if not seguimiento:
            raise NotFoundError('No sigues a este usuario')
        
        db.session.delete(seguimiento)
        db.session.commit()
        
        return {'message': 'Dejaste de seguir al usuario'}
    
    @staticmethod
    def seguir_semillero(semillero_id, usuario_id):
        """Seguir semillero"""
        existente = SeguimientoSemillero.query.filter_by(
            usuario_id=usuario_id,
            semillero_id=semillero_id
        ).first()
        
        if existente:
            raise ConflictError('Ya sigues este semillero')
        
        seguimiento = SeguimientoSemillero(
            usuario_id=usuario_id,
            semillero_id=semillero_id
        )
        
        db.session.add(seguimiento)
        db.session.commit()
        
        return seguimiento
    
    @staticmethod
    def listar_notificaciones(usuario_id, limit=50, offset=0, solo_no_leidas=False):
        """Listar notificaciones de usuario"""
        query = Notificacion.query.filter_by(usuario_id=usuario_id)
        
        if solo_no_leidas:
            query = query.filter(Notificacion.leida == False)
        
        notificaciones = query.order_by(Notificacion.creado_en.desc()).limit(limit).offset(offset).all()
        total = query.count()
        
        return notificaciones, total
    
    @staticmethod
    def marcar_notificacion_leida(notificacion_id, usuario_id):
        """Marcar notificación como leída"""
        notificacion = Notificacion.query.get(notificacion_id)
        if not notificacion:
            raise NotFoundError('Notificación no encontrada')
        
        if notificacion.usuario_id != usuario_id:
            raise ValidationError('Solo puedes marcar tus propias notificaciones')
        
        notificacion.leida = True
        notificacion.fecha_lectura = datetime.utcnow()
        db.session.commit()
        
        return notificacion
    
    @staticmethod
    def _crear_notificacion(usuario_id, tipo, mensaje, referencia_tipo=None, referencia_id=None):
        """Crear notificación (método interno)"""
        notificacion = Notificacion(
            usuario_id=usuario_id,
            tipo=tipo,
            titulo=tipo,
            mensaje=mensaje,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id
        )
        db.session.add(notificacion)
    
    @staticmethod
    def _otorgar_xp(usuario_id, tipo_actividad, referencia_tipo=None, referencia_id=None):
        """Otorgar XP (método interno)"""
        tipo = TipoActividadXP.query.filter_by(tipo=tipo_actividad).first()
        if not tipo:
            return
        
        movimiento = MovimientoXP(
            usuario_id=usuario_id,
            tipo_actividad_id=tipo.id,
            xp_ganada=tipo.xp_base,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id
        )
        db.session.add(movimiento)
        
        usuario = Usuario.query.get(usuario_id)
        usuario.xp_total += tipo.xp_base
        
        # Recalcular nivel
        from app.services.usuarios import UsuarioService
        UsuarioService._recalcular_nivel(usuario)
