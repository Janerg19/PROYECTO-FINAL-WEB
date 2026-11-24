from datetime import datetime
from app.extensions import db


class Evento(db.Model):
    """Eventos académicos"""
    __tablename__ = 'evento'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_evento = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(10))  # HH:MM
    lugar = db.Column(db.String(200))
    creado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_evento_fecha', 'fecha_evento'),
        db.Index('idx_evento_creador', 'creado_por'),
    )
    
    # Relaciones
    creador = db.relationship('Usuario', back_populates='eventos')
    participaciones = db.relationship('ParticipacionEvento', back_populates='evento', cascade='all, delete-orphan')


class ParticipacionEvento(db.Model):
    """Participación en eventos"""
    __tablename__ = 'participacion_evento'
    
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    rol = db.Column(db.String(50), default='asistente')  # asistente, ponente, organizador
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_participacion_evento', 'evento_id'),
        db.Index('idx_participacion_usuario', 'usuario_id'),
        db.UniqueConstraint('evento_id', 'usuario_id', name='uq_participacion_evento'),
    )
    
    # Relaciones
    evento = db.relationship('Evento', back_populates='participaciones')
    usuario = db.relationship('Usuario', back_populates='participaciones')


class Convocatoria(db.Model):
    """Convocatorias"""
    __tablename__ = 'convocatoria'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.String(20), nullable=False, default='borrador')
    fecha_apertura = db.Column(db.Date, nullable=False)
    fecha_cierre = db.Column(db.Date, nullable=False)
    validado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'))
    fecha_validacion = db.Column(db.DateTime)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_convocatoria_estado', 'estado'),
        db.Index('idx_convocatoria_fechas', 'fecha_apertura', 'fecha_cierre'),
    )
    
    # Relaciones
    validador = db.relationship('Usuario', foreign_keys=[validado_por])
    creador = db.relationship('Usuario', foreign_keys=[creado_por], back_populates='convocatorias')
    postulaciones = db.relationship('PostulacionConvocatoria', back_populates='convocatoria', cascade='all, delete-orphan')


class PostulacionConvocatoria(db.Model):
    """Postulaciones a convocatorias"""
    __tablename__ = 'postulacion_convocatoria'
    
    id = db.Column(db.Integer, primary_key=True)
    convocatoria_id = db.Column(db.Integer, db.ForeignKey('convocatoria.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    propuesta = db.Column(db.Text)
    estado = db.Column(db.String(20), nullable=False, default='enviada')
    fecha_postulacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_resolucion = db.Column(db.DateTime)
    revisado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'))
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_postulacion_convocatoria', 'convocatoria_id'),
        db.Index('idx_postulacion_usuario', 'usuario_id'),
        db.Index('idx_postulacion_estado', 'estado'),
        db.UniqueConstraint('convocatoria_id', 'usuario_id', name='uq_postulacion_convocatoria'),
    )
    
    # Relaciones
    convocatoria = db.relationship('Convocatoria', back_populates='postulaciones')
    usuario = db.relationship('Usuario', back_populates='postulaciones')
    revisor = db.relationship('Usuario', foreign_keys=[revisado_por])
