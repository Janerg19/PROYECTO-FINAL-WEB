from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.investigacion import (
    Facultad, Programa, LineaInvestigacion, Semillero, SemilleroLinea,
    SemilleroIntegrante, Proyecto, ProyectoIntegrante, AvanceProyecto, Producto
)


class FacultadSchema(Schema):
    """Schema para Facultad"""
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    codigo = fields.Str(required=True)


class ProgramaSchema(SQLAlchemyAutoSchema):
    """Schema para Programa"""
    class Meta:
        model = Programa
        load_instance = True
        include = ('nombre', 'codigo', 'tipo')
    
    facultad = fields.Nested(FacultadSchema, dump_only=True)


class LineaInvestigacionSchema(Schema):
    """Schema para LineaInvestigacion"""
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    descripcion = fields.Str()


class SemilleroSchema(SQLAlchemyAutoSchema):
    """Schema para Semillero"""
    class Meta:
        model = Semillero
        load_instance = True
        include = ('nombre', 'descripcion', 'fecha_creacion', 'activo')
    
    facultad = fields.Nested(FacultadSchema, dump_only=True)
    programa = fields.Nested(ProgramaSchema, dump_only=True)
    lider = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class SemilleroLineaSchema(SQLAlchemyAutoSchema):
    """Schema para SemilleroLinea"""
    class Meta:
        model = SemilleroLinea
        load_instance = True
    
    linea = fields.Nested(LineaInvestigacionSchema, dump_only=True)


class SemilleroIntegranteSchema(SQLAlchemyAutoSchema):
    """Schema para SemilleroIntegrante"""
    class Meta:
        model = SemilleroIntegrante
        load_instance = True
        include = ('rol', 'estado', 'fecha_solicitud', 'fecha_resolucion')
    
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    semillero = fields.Nested(SemilleroSchema, dump_only=True)


class ProyectoSchema(SQLAlchemyAutoSchema):
    """Schema para Proyecto"""
    class Meta:
        model = Proyecto
        load_instance = True
        include = ('titulo', 'descripcion', 'estado', 'fecha_inicio', 'fecha_fin')
    
    semillero = fields.Nested(SemilleroSchema, dump_only=True)


class ProyectoIntegranteSchema(SQLAlchemyAutoSchema):
    """Schema para ProyectoIntegrante"""
    class Meta:
        model = ProyectoIntegrante
        load_instance = True
        include = ('rol',)
    
    usuario = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)
    proyecto = fields.Nested(ProyectoSchema, dump_only=True)


class AvanceProyectoSchema(SQLAlchemyAutoSchema):
    """Schema para AvanceProyecto"""
    class Meta:
        model = AvanceProyecto
        load_instance = True
        include = ('titulo', 'descripcion', 'fecha_avance')
    
    proyecto = fields.Nested(ProyectoSchema, dump_only=True)
    creador = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


class ProductoSchema(SQLAlchemyAutoSchema):
    """Schema para Producto"""
    class Meta:
        model = Producto
        load_instance = True
        include = ('titulo', 'tipo', 'descripcion', 'fecha_publicacion', 'url')
    
    proyecto = fields.Nested(ProyectoSchema, dump_only=True)
    creador = fields.Nested('schemas.usuarios.UsuarioSchema', dump_only=True)


# Schemas de validación
class SemilleroCreateSchema(Schema):
    """Schema para crear semillero"""
    nombre = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    descripcion = fields.Str()
    facultad_id = fields.Int(required=True)
    programa_id = fields.Int()
    lider_id = fields.Int(required=True)


class SemilleroUpdateSchema(Schema):
    """Schema para actualizar semillero"""
    nombre = fields.Str(validate=lambda x: len(x) >= 3)
    descripcion = fields.Str()
    activo = fields.Bool()


class VinculacionSchema(Schema):
    """Schema para solicitud de vinculación"""
    semillero_id = fields.Int(required=True)


class VinculacionResolucionSchema(Schema):
    """Schema para resolver vinculación"""
    estado = fields.Str(required=True, validate=validate.OneOf(['aprobada', 'rechazada']))


class ProyectoCreateSchema(Schema):
    """Schema para crear proyecto"""
    titulo = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    descripcion = fields.Str()
    semillero_id = fields.Int(required=True)
    estado = fields.Str(validate=validate.OneOf(['formulacion', 'en_curso', 'finalizado']))
    fecha_inicio = fields.Date()
    fecha_fin = fields.Date()
