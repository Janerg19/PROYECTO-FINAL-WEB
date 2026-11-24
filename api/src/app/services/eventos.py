from datetime import datetime
from app.extensions import db
from app.models.eventos import Evento, ParticipacionEvento, Convocatoria, PostulacionConvocatoria
from app.models.usuarios import Usuario
from app.utils.errors import ValidationError, NotFoundError, ConflictError


class EventosService:
    """Servicio de lógica de negocio para eventos"""
    
    @staticmethod
    def listar_eventos(limit=50, offset=0):
        """Listar eventos"""
        query = Evento.query
        eventos = query.order_by(Evento.fecha_evento.desc()).limit(limit).offset(offset).all()
        total = query.count()
        return eventos, total
    
    @staticmethod
    def crear_evento(data, creador_id):
        """Crear evento"""
        evento = Evento(
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            fecha_evento=data['fecha_evento'],
            hora=data.get('hora'),
            lugar=data.get('lugar'),
            creado_por=creador_id
        )
        db.session.add(evento)
        db.session.commit()
        return evento
    
    @staticmethod
    def participar_evento(evento_id, usuario_id, rol='asistente'):
        """Participar en evento"""
        existente = ParticipacionEvento.query.filter_by(
            evento_id=evento_id,
            usuario_id=usuario_id
        ).first()
        if existente:
            raise ConflictError('Ya estás participando en este evento')
        
        participacion = ParticipacionEvento(
            evento_id=evento_id,
            usuario_id=usuario_id,
            rol=rol
        )
        db.session.add(participacion)
        db.session.commit()
        return participacion
    
    @staticmethod
    def listar_convocatorias(limit=50, offset=0, estado=None):
        """Listar convocatorias"""
        query = Convocatoria.query
        if estado:
            query = query.filter(Convocatoria.estado == estado)
        convocatorias = query.order_by(Convocatoria.fecha_apertura.desc()).limit(limit).offset(offset).all()
        total = query.count()
        return convocatorias, total
    
    @staticmethod
    def crear_convocatoria(data, creador_id):
        """Crear convocatoria (solo admin)"""
        creador = Usuario.query.get(creador_id)
        if not creador or creador.rol.nombre != 'administrador':
            raise ValidationError('Solo administradores pueden crear convocatorias')
        
        convocatoria = Convocatoria(
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            estado=data.get('estado', 'borrador'),
            fecha_apertura=data['fecha_apertura'],
            fecha_cierre=data['fecha_cierre'],
            creado_por=creador_id
        )
        db.session.add(convocatoria)
        db.session.commit()
        return convocatoria
    
    @staticmethod
    def validar_convocatoria(convocatoria_id, admin_id):
        """Validar convocatoria (solo admin)"""
        convocatoria = Convocatoria.query.get(convocatoria_id)
        if not convocatoria:
            raise NotFoundError('Convocatoria no encontrada')
        
        convocatoria.estado = 'publicada'
        convocatoria.validado_por = admin_id
        convocatoria.fecha_validacion = datetime.utcnow()
        db.session.commit()
        return convocatoria
    
    @staticmethod
    def postular_convocatoria(convocatoria_id, propuesta, usuario_id):
        """Postular a convocatoria"""
        # Verificar que la convocatoria esté abierta
        convocatoria = Convocatoria.query.get(convocatoria_id)
        if not convocatoria or convocatoria.estado != 'publicada':
            raise ValidationError('La convocatoria no está abierta')
        
        hoy = datetime.utcnow().date()
        if hoy < convocatoria.fecha_apertura or hoy > convocatoria.fecha_cierre:
            raise ValidationError('La convocatoria no está en periodo de postulación')
        
        # Verificar que no exista postulación previa
        existente = PostulacionConvocatoria.query.filter_by(
            convocatoria_id=convocatoria_id,
            usuario_id=usuario_id
        ).first()
        if existente:
            raise ConflictError('Ya has postulado a esta convocatoria')
        
        postulacion = PostulacionConvocatoria(
            convocatoria_id=convocatoria_id,
            usuario_id=usuario_id,
            propuesta=propuesta,
            estado='enviada'
        )
        db.session.add(postulacion)
        db.session.commit()
        return postulacion
    
    @staticmethod
    def listar_postulaciones(limit=50, offset=0):
        """Listar postulaciones (solo admin)"""
        query = PostulacionConvocatoria.query
        postulaciones = query.order_by(PostulacionConvocatoria.fecha_postulacion.desc()).limit(limit).offset(offset).all()
        total = query.count()
        return postulaciones, total
    
    @staticmethod
    def resolver_postulacion(postulacion_id, estado, admin_id):
        """Resolver postulación (solo admin)"""
        postulacion = PostulacionConvocatoria.query.get(postulacion_id)
        if not postulacion:
            raise NotFoundError('Postulación no encontrada')
        
        if postulacion.estado != 'enviada':
            raise ValidationError('Solo se pueden resolver postulaciones enviadas')
        
        postulacion.estado = estado
        postulacion.fecha_resolucion = datetime.utcnow()
        postulacion.revisado_por = admin_id
        
        # Notificar al usuario
        from app.services.gamificacion import GamificacionService
        mensaje = f'Tu postulación ha sido {estado}' if estado == 'aprobada' else f'Tu postulación ha sido rechazada'
        GamificacionService._crear_notificacion(
            postulacion.usuario_id,
            'postulacion_resolucion',
            mensaje,
            referencia_tipo='postulacion',
            referencia_id=postulacion.id
        )
        
        db.session.commit()
        return postulacion
