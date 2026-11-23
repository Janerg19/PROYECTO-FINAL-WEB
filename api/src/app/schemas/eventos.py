from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.eventos import Evento, ParticipacionEvento, Convocatoria, PostulacionConvocatoria


class EventoSchema(SQLAlchemyAutoSchema):
    """Schema para Evento"""
    class Meta:
        model = Evento
        load_instance = True
        include = ('titulo', 'descripcion', 'fecha_evento', 'hora', 'lugar')
    
    creador = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class ParticipacionEventoSchema(SQLAlchemyAutoSchema):
    """Schema para ParticipacionEvento"""
    class Meta:
        model = ParticipacionEvento
        load_instance = True
        include = ('rol',)
    
    evento = fields.Nested(EventoSchema, dump_only=True)
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class ConvocatoriaSchema(SQLAlchemyAutoSchema):
    """Schema para Convocatoria"""
    class Meta:
        model = Convocatoria
        load_instance = True
        include = ('titulo', 'descripcion', 'estado', 'fecha_apertura', 'fecha_cierre')
    
    validador = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    creador = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class PostulacionConvocatoriaSchema(SQLAlchemyAutoSchema):
    """Schema para PostulacionConvocatoria"""
    class Meta:
        model = PostulacionConvocatoria
        load_instance = True
        include = ('propuesta', 'estado', 'fecha_postulacion', 'fecha_resolucion')
    
    convocatoria = fields.Nested(ConvocatoriaSchema, dump_only=True)
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    revisor = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


# Schemas de validación
class EventoCreateSchema(Schema):
    """Schema para crear evento"""
    titulo = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    descripcion = fields.Str()
    fecha_evento = fields.Date(required=True)
    hora = fields.Str(validate=lambda x: len(x) == 5 if x else True)  # HH:MM
    lugar = fields.Str()


class ConvocatoriaCreateSchema(Schema):
    """Schema para crear convocatoria"""
    titulo = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    descripcion = fields.Str()
    fecha_apertura = fields.Date(required=True)
    fecha_cierre = fields.Date(required=True)
    estado = fields.Str(validate=validate.OneOf(['borrador', 'publicada', 'cerrada']))


class PostulacionCreateSchema(Schema):
    """Schema para postular a convocatoria"""
    propuesta = fields.Str(required=True)


class PostulacionResolucionSchema(Schema):
    """Schema para resolver postulación"""
    estado = fields.Str(required=True, validate=validate.OneOf(['aprobada', 'rechazada']))
