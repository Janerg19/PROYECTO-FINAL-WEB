from datetime import datetime
from app.extensions import db


class CategoriaPublicacion(db.Model):
    """Categorías de publicación"""
    __tablename__ = 'categoria_publicacion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    color = db.Column(db.String(20))
    
    # Relaciones
    publicaciones = db.relationship('Publicacion', back_populates='categoria')


class Evidencia(db.Model):
    """Evidencias (archivos adjuntos)"""
    __tablename__ = 'evidencia'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    tipo_mime = db.Column(db.String(100), nullable=False)
    tamano_bytes = db.Column(db.BigInteger, nullable=False)
    ruta = db.Column(db.String(500), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_evidencia_ruta', 'ruta'),
    )
    
    # Relaciones
    publicaciones = db.relationship('PublicacionEvidencia', back_populates='evidencia')
    logros = db.relationship('LogroEvidencia', back_populates='evidencia')


class Publicacion(db.Model):
    """Publicaciones del feed social"""
    __tablename__ = 'publicacion'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_publicacion.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    semillero_id = db.Column(db.Integer, db.ForeignKey('semillero.id', ondelete='SET NULL', onupdate='CASCADE'))
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    eliminado_en = db.Column(db.DateTime)
    
    # Índices
    __table_args__ = (
        db.Index('idx_publicacion_usuario', 'usuario_id'),
        db.Index('idx_publicacion_semillero', 'semillero_id'),
        db.Index('idx_publicacion_categoria', 'categoria_id'),
        db.Index('idx_publicacion_fecha', 'creado_en'),
    )
    
    # Relaciones
    categoria = db.relationship('CategoriaPublicacion', back_populates='publicaciones')
    usuario = db.relationship('Usuario', back_populates='publicaciones')
    semillero = db.relationship('Semillero', back_populates='publicaciones')
    comentarios = db.relationship('Comentario', back_populates='publicacion', cascade='all, delete-orphan')
    reacciones = db.relationship('Reaccion', back_populates='publicacion', cascade='all, delete-orphan')
    compartidos = db.relationship('Compartido', back_populates='publicacion', cascade='all, delete-orphan')
    evidencias = db.relationship('PublicacionEvidencia', back_populates='publicacion', cascade='all, delete-orphan')


class PublicacionEvidencia(db.Model):
    """Relación publicación-evidencia"""
    __tablename__ = 'publicacion_evidencia'
    
    id = db.Column(db.Integer, primary_key=True)
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicacion.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    evidencia_id = db.Column(db.Integer, db.ForeignKey('evidencia.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_pub_evidencia_publicacion', 'publicacion_id'),
        db.Index('idx_pub_evidencia_evidencia', 'evidencia_id'),
        db.UniqueConstraint('publicacion_id', 'evidencia_id', name='uq_publicacion_evidencia'),
    )
    
    # Relaciones
    publicacion = db.relationship('Publicacion', back_populates='evidencias')
    evidencia = db.relationship('Evidencia', back_populates='publicaciones')


class Comentario(db.Model):
    """Comentarios en publicaciones"""
    __tablename__ = 'comentario'
    
    id = db.Column(db.Integer, primary_key=True)
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicacion.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    eliminado_en = db.Column(db.DateTime)
    
    # Índices
    __table_args__ = (
        db.Index('idx_comentario_publicacion', 'publicacion_id'),
        db.Index('idx_comentario_usuario', 'usuario_id'),
        db.Index('idx_comentario_fecha', 'creado_en'),
    )
    
    # Relaciones
    publicacion = db.relationship('Publicacion', back_populates='comentarios')
    usuario = db.relationship('Usuario', back_populates='comentarios')


class Reaccion(db.Model):
    """Reacciones a publicaciones"""
    __tablename__ = 'reaccion'
    
    id = db.Column(db.Integer, primary_key=True)
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicacion.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_reaccion_publicacion', 'publicacion_id'),
        db.Index('idx_reaccion_usuario', 'usuario_id'),
        db.Index('idx_reaccion_tipo', 'tipo'),
        db.UniqueConstraint('publicacion_id', 'usuario_id', 'tipo', name='uq_reaccion'),
    )
    
    # Relaciones
    publicacion = db.relationship('Publicacion', back_populates='reacciones')
    usuario = db.relationship('Usuario', back_populates='reacciones')


class Compartido(db.Model):
    """Compartidos de publicaciones"""
    __tablename__ = 'compartido'
    
    id = db.Column(db.Integer, primary_key=True)
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicacion.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_compartido_publicacion', 'publicacion_id'),
        db.Index('idx_compartido_usuario', 'usuario_id'),
        db.UniqueConstraint('publicacion_id', 'usuario_id', name='uq_compartido'),
    )
    
    # Relaciones
    publicacion = db.relationship('Publicacion', back_populates='compartidos')
    usuario = db.relationship('Usuario', back_populates='compartidos')


class SeguimientoUsuario(db.Model):
    """Seguimiento entre usuarios"""
    __tablename__ = 'seguimiento_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    seguidor_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    seguido_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_seguimiento_seguidor', 'seguidor_id'),
        db.Index('idx_seguimiento_seguido', 'seguido_id'),
        db.UniqueConstraint('seguidor_id', 'seguido_id', name='uq_seguimiento_usuario'),
        db.CheckConstraint('seguidor_id != seguido_id', name='chk_no_auto_seguimiento'),
    )
    
    # Relaciones
    seguidor = db.relationship('Usuario', foreign_keys=[seguidor_id], back_populates='seguidores')
    seguido = db.relationship('Usuario', foreign_keys=[seguido_id], back_populates='seguidos')


class SeguimientoSemillero(db.Model):
    """Seguimiento de semilleros"""
    __tablename__ = 'seguimiento_semillero'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    semillero_id = db.Column(db.Integer, db.ForeignKey('semillero.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_seguimiento_semillero_usuario', 'usuario_id'),
        db.Index('idx_seguimiento_semillero_semillero', 'semillero_id'),
        db.UniqueConstraint('usuario_id', 'semillero_id', name='uq_seguimiento_semillero'),
    )
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='seguimientos_semillero')
    semillero = db.relationship('Semillero', back_populates='seguimientos')


class Notificacion(db.Model):
    """Notificaciones para usuarios"""
    __tablename__ = 'notificacion'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text)
    leida = db.Column(db.Boolean, nullable=False, default=False)
    fecha_lectura = db.Column(db.DateTime)
    referencia_tipo = db.Column(db.String(50))
    referencia_id = db.Column(db.Integer)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_notificacion_usuario', 'usuario_id'),
        db.Index('idx_notificacion_leida', 'usuario_id', 'leida'),
        db.Index('idx_notificacion_fecha', 'creado_en'),
    )
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='notificaciones')
