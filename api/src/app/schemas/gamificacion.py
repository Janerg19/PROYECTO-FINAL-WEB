from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.gamificacion import TipoActividadXP, Logro, LogroEvidencia, MovimientoXP


class TipoActividadXPSchema(Schema):
    """Schema para TipoActividadXP"""
    id = fields.Int(dump_only=True)
    tipo = fields.Str(required=True)
    xp_base = fields.Int(required=True)
    descripcion = fields.Str()


class LogroSchema(SQLAlchemyAutoSchema):
    """Schema para Logro"""
    class Meta:
        model = Logro
        load_instance = True
        include = ('tipo', 'titulo', 'descripcion', 'estado', 'fecha_validacion')
    
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    validador = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class MovimientoXPSchema(SQLAlchemyAutoSchema):
    """Schema para MovimientoXP"""
    class Meta:
        model = MovimientoXP
        load_instance = True
        include = ('xp_ganada', 'referencia_tipo', 'referencia_id', 'creado_en')
    
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    tipo_actividad = fields.Nested(TipoActividadXPSchema, dump_only=True)


class GamificacionMeSchema(Schema):
    """Schema para GET /api/gamificacion/me"""
    xp_total = fields.Int(required=True)
    nivel = fields.Nested('schemas.usuarios.NivelSchema')
    estrellas = fields.Int()
    insignias = fields.List(fields.Nested('schemas.usuarios.InsigniaSchema'))
    historial_xp = fields.List(fields.Nested(MovimientoXPSchema))


# Schemas de validación
class LogroCreateSchema(Schema):
    """Schema para enviar logro"""
    tipo = fields.Str(required=True, validate=lambda x: len(x) >= 2)
    titulo = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    descripcion = fields.Str()


class LogroResolucionSchema(Schema):
    """Schema para resolver logro"""
    estado = fields.Str(required=True, validate=validate.OneOf(['validado', 'rechazado']))
