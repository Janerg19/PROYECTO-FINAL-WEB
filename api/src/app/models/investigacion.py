from datetime import datetime
from extensions import db


class Facultad(db.Model):
    """Facultades"""
    __tablename__ = 'facultad'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(10), nullable=False)
    
    # Relaciones
    programas = db.relationship('Programa', back_populates='facultad')
    semilleros = db.relationship('Semillero', back_populates='facultad')


class Programa(db.Model):
    """Programas académicos"""
    __tablename__ = 'programa'
    
    id = db.Column(db.Integer, primary_key=True)
    facultad_id = db.Column(db.Integer, db.ForeignKey('facultad.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    
    # Relaciones
    facultad = db.relationship('Facultad', back_populates='programas')
    usuarios = db.relationship('UsuarioPrograma', back_populates='programa')
    semilleros = db.relationship('Semillero', back_populates='programa')


class LineaInvestigacion(db.Model):
    """Líneas de investigación"""
    __tablename__ = 'linea_investigacion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relaciones
    semilleros = db.relationship('SemilleroLinea', back_populates='linea')


class Semillero(db.Model):
    """Semilleros de investigación"""
    __tablename__ = 'semillero'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    facultad_id = db.Column(db.Integer, db.ForeignKey('facultad.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    programa_id = db.Column(db.Integer, db.ForeignKey('programa.id', ondelete='SET NULL', onupdate='CASCADE'))
    lider_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    eliminado_en = db.Column(db.DateTime)
    
    # Índices
    __table_args__ = (
        db.Index('idx_semillero_facultad', 'facultad_id'),
        db.Index('idx_semillero_programa', 'programa_id'),
        db.Index('idx_semillero_lider', 'lider_id'),
        db.Index('idx_semillero_activo', 'activo'),
    )
    
    # Relaciones
    facultad = db.relationship('Facultad', back_populates='semilleros')
    programa = db.relationship('Programa', back_populates='semilleros')
    lider = db.relationship('Usuario', back_populates='semilleros_lider')
    lineas = db.relationship('SemilleroLinea', back_populates='semillero', cascade='all, delete-orphan')
    integrantes = db.relationship('SemilleroIntegrante', back_populates='semillero', cascade='all, delete-orphan')
    proyectos = db.relationship('Proyecto', back_populates='semillero', cascade='all, delete-orphan')
    publicaciones = db.relationship('Publicacion', back_populates='semillero')
    seguimientos = db.relationship('SeguimientoSemillero', back_populates='semillero', cascade='all, delete-orphan')


class SemilleroLinea(db.Model):
    """Relación semillero-línea de investigación"""
    __tablename__ = 'semillero_linea'
    
    id = db.Column(db.Integer, primary_key=True)
    semillero_id = db.Column(db.Integer, db.ForeignKey('semillero.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    linea_id = db.Column(db.Integer, db.ForeignKey('linea_investigacion.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_semillero_linea_semillero', 'semillero_id'),
        db.Index('idx_semillero_linea_linea', 'linea_id'),
        db.UniqueConstraint('semillero_id', 'linea_id', name='uq_semillero_linea'),
    )
    
    # Relaciones
    semillero = db.relationship('Semillero', back_populates='lineas')
    linea = db.relationship('LineaInvestigacion', back_populates='semilleros')


class SemilleroIntegrante(db.Model):
    """Integrantes de semillero"""
    __tablename__ = 'semillero_integrante'
    
    id = db.Column(db.Integer, primary_key=True)
    semillero_id = db.Column(db.Integer, db.ForeignKey('semillero.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='estudiante')
    estado = db.Column(db.String(20), nullable=False, default='solicitada')
    fecha_solicitud = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_resolucion = db.Column(db.DateTime)
    revisado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'))
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_semillero_integrante_semillero', 'semillero_id'),
        db.Index('idx_semillero_integrante_usuario', 'usuario_id'),
        db.Index('idx_semillero_integrante_estado', 'estado'),
        db.UniqueConstraint('semillero_id', 'usuario_id', name='uq_semillero_integrante'),
    )
    
    # Relaciones
    semillero = db.relationship('Semillero', back_populates='integrantes')
    usuario = db.relationship('Usuario', back_populates='semilleros_integrante')
    revisor = db.relationship('Usuario', foreign_keys=[revisado_por])


class Proyecto(db.Model):
    """Proyectos de investigación"""
    __tablename__ = 'proyecto'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    semillero_id = db.Column(db.Integer, db.ForeignKey('semillero.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='formulacion')
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    eliminado_en = db.Column(db.DateTime)
    
    # Índices
    __table_args__ = (
        db.Index('idx_proyecto_semillero', 'semillero_id'),
        db.Index('idx_proyecto_estado', 'estado'),
    )
    
    # Relaciones
    semillero = db.relationship('Semillero', back_populates='proyectos')
    integrantes = db.relationship('ProyectoIntegrante', back_populates='proyecto', cascade='all, delete-orphan')
    avances = db.relationship('AvanceProyecto', back_populates='proyecto', cascade='all, delete-orphan')
    productos = db.relationship('Producto', back_populates='proyecto')


class ProyectoIntegrante(db.Model):
    """Integrantes de proyecto"""
    __tablename__ = 'proyecto_integrante'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    rol = db.Column(db.String(50), default='investigador')
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_proyecto_integrante_proyecto', 'proyecto_id'),
        db.Index('idx_proyecto_integrante_usuario', 'usuario_id'),
        db.UniqueConstraint('proyecto_id', 'usuario_id', name='uq_proyecto_integrante'),
    )
    
    # Relaciones
    proyecto = db.relationship('Proyecto', back_populates='integrantes')
    usuario = db.relationship('Usuario', back_populates='proyectos')


class AvanceProyecto(db.Model):
    """Avances de proyecto"""
    __tablename__ = 'avance_proyecto'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_avance = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_avance_proyecto', 'proyecto_id'),
        db.Index('idx_avance_fecha', 'fecha_avance'),
    )
    
    # Relaciones
    proyecto = db.relationship('Proyecto', back_populates='avances')
    creador = db.relationship('Usuario', back_populates='avances')


class Producto(db.Model):
    """Productos de investigación"""
    __tablename__ = 'producto'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id', ondelete='SET NULL', onupdate='CASCADE'))
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_publicacion = db.Column(db.Date)
    url = db.Column(db.String(500))
    creado_por = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=False)
    creado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        db.Index('idx_producto_proyecto', 'proyecto_id'),
        db.Index('idx_producto_tipo', 'tipo'),
        db.Index('idx_producto_creador', 'creado_por'),
    )
    
    # Relaciones
    proyecto = db.relationship('Proyecto', back_populates='productos')
    creador = db.relationship('Usuario', back_populates='productos')
