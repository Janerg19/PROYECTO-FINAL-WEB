from datetime import datetime
from app.extensions import db


class Rol(db.Model):
    """Roles del sistema"""
    __tablename__ = 'rol'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    usuarios = db.relationship('Usuario', back_populates='rol', lazy='dynamic')


class Usuario(db.Model):
    """Usuarios del sistema"""
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    validado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'))
    fecha_validacion = db.Column(db.DateTime)
    documento_ruta = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    eliminado_en = db.Column(db.DateTime)
    xp_total = db.Column(db.Integer, nullable=False, default=0)
    nivel_id = db.Column(db.Integer, db.ForeignKey('nivel.id', ondelete='SET NULL', onupdate='CASCADE'))
    
    # Índices
    __table_args__ = (
        db.Index('idx_usuario_email', 'email'),
        db.Index('idx_usuario_estado', 'estado'),
        db.Index('idx_usuario_rol', 'rol_id'),
        db.Index('idx_usuario_nombre', 'nombres', 'apellidos'),
        db.Index('idx_usuario_xp_total', 'xp_total'),
    )
    
    # Relaciones
    rol = db.relationship('Rol', back_populates='usuarios')
    perfil_investigador = db.relationship('PerfilInvestigador', back_populates='usuario', uselist=False, cascade='all, delete-orphan')
    programas = db.relationship('UsuarioPrograma', back_populates='usuario', cascade='all, delete-orphan')
    semilleros_lider = db.relationship('Semillero', back_populates='lider')
    semilleros_integrante = db.relationship('SemilleroIntegrante', back_populates='usuario', cascade='all, delete-orphan')
    proyectos = db.relationship('ProyectoIntegrante', back_populates='usuario', cascade='all, delete-orphan')
    eventos = db.relationship('Evento', back_populates='creador')
    participaciones = db.relationship('ParticipacionEvento', back_populates='usuario', cascade='all, delete-orphan')
    convocatorias = db.relationship('Convocatoria', back_populates='creador')
    postulaciones = db.relationship('PostulacionConvocatoria', back_populates='usuario', cascade='all, delete-orphan')
    publicaciones = db.relationship('Publicacion', back_populates='usuario', cascade='all, delete-orphan')
    comentarios = db.relationship('Comentario', back_populates='usuario', cascade='all, delete-orphan')
    reacciones = db.relationship('Reaccion', back_populates='usuario', cascade='all, delete-orphan')
    compartidos = db.relationship('Compartido', back_populates='usuario', cascade='all, delete-orphan')
    seguidores = db.relationship('SeguimientoUsuario', foreign_keys='SeguimientoUsuario.seguidor_id', back_populates='seguidor', cascade='all, delete-orphan')
    seguidos = db.relationship('SeguimientoUsuario', foreign_keys='SeguimientoUsuario.seguido_id', back_populates='seguido', cascade='all, delete-orphan')
    seguimientos_semillero = db.relationship('SeguimientoSemillero', back_populates='usuario', cascade='all, delete-orphan')
    notificaciones = db.relationship('Notificacion', back_populates='usuario', cascade='all, delete-orphan')
    logros = db.relationship('Logro', back_populates='usuario', cascade='all, delete-orphan')
    movimientos_xp = db.relationship('MovimientoXP', back_populates='usuario', cascade='all, delete-orphan')
    insignias = db.relationship('UsuarioInsignia', back_populates='usuario', cascade='all, delete-orphan')
    validaciones = db.relationship('Usuario', remote_side=[id], foreign_keys='validado_por')
    validaciones_logros = db.relationship('Logro', foreign_keys='validado_por')
    validaciones_convocatorias = db.relationship('Convocatoria', foreign_keys='validado_por')
    validaciones_postulaciones = db.relationship('PostulacionConvocatoria', foreign_keys='revisado_por')
    validaciones_vinculaciones = db.relationship('SemilleroIntegrante', foreign_keys='revisado_por')
    avances = db.relationship('AvanceProyecto', back_populates='creador')
    productos = db.relationship('Producto', back_populates='creador')


class PerfilInvestigador(db.Model):
    """Perfil investigativo del usuario"""
    __tablename__ = 'perfil_investigador'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), unique=True, nullable=False)
    biografia = db.Column(db.Text)
    intereses = db.Column(db.JSON)  # Array de intereses almacenado como JSON
    orcid = db.Column(db.String(50))
    cvlac = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_perfil_usuario', 'usuario_id'),
    )
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='perfil_investigador')


class UsuarioPrograma(db.Model):
    """Relación usuario-programa"""
    __tablename__ = 'usuario_programa'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    programa_id = db.Column(db.Integer, db.ForeignKey('programa.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    actual = db.Column(db.Boolean, nullable=False, default=True)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_usuario_programa_usuario', 'usuario_id'),
        db.Index('idx_usuario_programa_programa', 'programa_id'),
        db.UniqueConstraint('usuario_id', 'programa_id', 'fecha_inicio', name='uq_usuario_programa'),
    )
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='programas')
    programa = db.relationship('Programa')


class Nivel(db.Model):
    """Niveles de gamificación"""
    __tablename__ = 'nivel'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    umbral_xp = db.Column(db.Integer, nullable=False)
    estrellas = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(100))
    
    # Relaciones
    usuarios = db.relationship('Usuario', backref='nivel')


class Insignia(db.Model):
    """Insignias de gamificación"""
    __tablename__ = 'insignia'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    criterio = db.Column(db.String(200))
    icono = db.Column(db.String(50))
    color = db.Column(db.String(20))
    
    # Relaciones
    usuarios = db.relationship('UsuarioInsignia', back_populates='insignia')


class UsuarioInsignia(db.Model):
    """Relación usuario-insignia"""
    __tablename__ = 'usuario_insignia'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    insignia_id = db.Column(db.Integer, db.ForeignKey('insignia.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    otorgada_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'))
    fecha_otorgamiento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_usuario_insignia_usuario', 'usuario_id'),
        db.Index('idx_usuario_insignia_insignia', 'insignia_id'),
        db.UniqueConstraint('usuario_id', 'insignia_id', name='uq_usuario_insignia'),
    )
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='insignias')
    insignia = db.relationship('Insignia', back_populates='usuarios')
    otorgador = db.relationship('Usuario', foreign_keys=[otorgada_por])
