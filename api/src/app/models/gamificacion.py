from datetime import datetime
from extensions import db


class TipoActividadXP(db.Model):
    """Tipos de actividad con XP"""
    __tablename__ = 'tipo_actividad_xp'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), unique=True, nullable=False)
    xp_base = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    movimientos = db.relationship('MovimientoXP', back_populates='tipo_actividad')


class Logro(db.Model):
    """Logros enviados por usuarios"""
    __tablename__ = 'logro'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.String(20), nullable=False, default='enviado')
    validado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'))
    fecha_validacion = db.Column(db.DateTime)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_logro_usuario', 'usuario_id'),
        db.Index('idx_logro_estado', 'estado'),
    )
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='logros')
    validador = db.relationship('Usuario', foreign_keys=[validado_por])
    evidencias = db.relationship('LogroEvidencia', back_populates='logro', cascade='all, delete-orphan')


class LogroEvidencia(db.Model):
    """Relación logro-evidencia"""
    __tablename__ = 'logro_evidencia'
    
    id = db.Column(db.Integer, primary_key=True)
    logro_id = db.Column(db.Integer, db.ForeignKey('logro.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    evidencia_id = db.Column(db.Integer, db.ForeignKey('evidencia.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_logro_evidencia_logro', 'logro_id'),
        db.Index('idx_logro_evidencia_evidencia', 'evidencia_id'),
        db.UniqueConstraint('logro_id', 'evidencia_id', name='uq_logro_evidencia'),
    )
    
    # Relaciones
    logro = db.relationship('Logro', back_populates='evidencias')
    evidencia = db.relationship('Evidencia', back_populates='logros')


class MovimientoXP(db.Model):
    """Historial inmutable de movimientos de XP"""
    __tablename__ = 'movimiento_xp'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tipo_actividad_id = db.Column(db.Integer, db.ForeignKey('tipo_actividad_xp.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    xp_ganada = db.Column(db.Integer, nullable=False)
    referencia_tipo = db.Column(db.String(50))
    referencia_id = db.Column(db.Integer)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_movimiento_usuario', 'usuario_id'),
        db.Index('idx_movimiento_fecha', 'creado_en'),
    )
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='movimientos_xp')
    tipo_actividad = db.relationship('TipoActividadXP', back_populates='movimientos')
