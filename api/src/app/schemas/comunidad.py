from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.comunidad import (
    CategoriaPublicacion, Evidencia, Publicacion, PublicacionEvidencia,
    Comentario, Reaccion, Compartido, SeguimientoUsuario,
    SeguimientoSemillero, Notificacion
)


class CategoriaPublicacionSchema(Schema):
    """Schema para CategoriaPublicacion"""
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    descripcion = fields.Str()
    color = fields.Str()


class EvidenciaSchema(SQLAlchemyAutoSchema):
    """Schema para Evidencia"""
    class Meta:
        model = Evidencia
        load_instance = True
        include = ('nombre_archivo', 'tipo_mime', 'tamano_bytes', 'ruta')


class PublicacionSchema(SQLAlchemyAutoSchema):
    """Schema para Publicacion"""
    class Meta:
        model = Publicacion
        load_instance = True
        include = ('titulo', 'contenido', 'creado_en')
    
    categoria = fields.Nested(CategoriaPublicacionSchema, dump_only=True)
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    semillero = fields.Nested('schemas.investigacion.SemilleroSchema', dump_only=True)


class ComentarioSchema(SQLAlchemyAutoSchema):
    """Schema para Comentario"""
    class Meta:
        model = Comentario
        load_instance = True
        include = ('contenido', 'creado_en')
    
    publicacion = fields.Nested(PublicacionSchema, dump_only=True)
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class ReaccionSchema(SQLAlchemyAutoSchema):
    """Schema para Reaccion"""
    class Meta:
        model = Reaccion
        load_instance = True
        include = ('tipo', 'creado_en')
    
    publicacion = fields.Nested(PublicacionSchema, dump_only=True)
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class SeguimientoUsuarioSchema(SQLAlchemyAutoSchema):
    """Schema para SeguimientoUsuario"""
    class Meta:
        model = SeguimientoUsuario
        load_instance = True
        include = ('creado_en',)
    
    seguidor = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    seguido = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class SeguimientoSemilleroSchema(SQLAlchemyAutoSchema):
    """Schema para SeguimientoSemillero"""
    class Meta:
        model = SeguimientoSemillero
        load_instance = True
        include = ('creado_en',)
    
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    semillero = fields.Nested('schemas.investigacion.SemilleroSchema', dump_only=True)


class NotificacionSchema(SQLAlchemyAutoSchema):
    """Schema para Notificacion"""
    class Meta:
        model = Notificacion
        load_instance = True
        include = ('tipo', 'titulo', 'mensaje', 'leida', 'fecha_lectura', 'creado_en')
    
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


# Schemas de validación
class PublicacionCreateSchema(Schema):
    """Schema para crear publicación"""
    titulo = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    contenido = fields.Str(required=True, validate=lambda x: len(x) >= 10)
    categoria_id = fields.Int(required=True)
    semillero_id = fields.Int()


class PublicacionUpdateSchema(Schema):
    """Schema para actualizar publicación"""
    titulo = fields.Str(validate=lambda x: len(x) >= 3)
    contenido = fields.Str(validate=lambda x: len(x) >= 10)
    categoria_id = fields.Int()


class ComentarioCreateSchema(Schema):
    """Schema para crear comentario"""
    contenido = fields.Str(required=True, validate=lambda x: len(x) >= 1)


class ReaccionCreateSchema(Schema):
    """Schema para crear reacción"""
    tipo = fields.Str(required=True, validate=validate.OneOf(['me_gusta', 'me_encanta', 'me_interesa']))


class NotificacionUpdateSchema(Schema):
    """Schema para marcar notificación como leída"""
    leida = fields.Bool(required=True)
