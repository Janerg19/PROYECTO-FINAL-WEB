from marshmallow import Schema, fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from extensions import db
from models.usuarios import Rol, Usuario, PerfilInvestigador, UsuarioPrograma, Nivel, Insignia, UsuarioInsignia


class RolSchema(Schema):
    """Schema para Rol"""
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    descripcion = fields.Str()


class UsuarioSchema(SQLAlchemyAutoSchema):
    """Schema para Usuario"""
    class Meta:
        model = Usuario
        load_instance = True
        exclude = ('password_hash',)  # Nunca exponer el hash
    
    # Campos calculados/relaciones
    rol = fields.Nested(RolSchema, dump_only=True)
    xp_total = fields.Int(dump_only=True)
    nivel_id = fields.Int(dump_only=True)


class PerfilInvestigadorSchema(SQLAlchemyAutoSchema):
    """Schema para PerfilInvestigador"""
    class Meta:
        model = PerfilInvestigador
        load_instance = True
        include = ('biografia', 'intereses', 'orcid', 'cvlac')


class UsuarioProgramaSchema(SQLAlchemyAutoSchema):
    """Schema para UsuarioPrograma"""
    class Meta:
        model = UsuarioPrograma
        load_instance = True
        include = ('fecha_inicio', 'fecha_fin', 'actual')


class NivelSchema(Schema):
    """Schema para Nivel"""
    id = fields.Int(dump_only=True)
    numero = fields.Int(required=True)
    umbral_xp = fields.Int(required=True)
    estrellas = fields.Int(required=True)
    description = fields.Str()


class InsigniaSchema(Schema):
    """Schema para Insignia"""
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    descripcion = fields.Str()
    criterio = fields.Str()
    icono = fields.Str()
    color = fields.Str()


class UsuarioInsigniaSchema(SQLAlchemyAutoSchema):
    """Schema para UsuarioInsignia"""
    class Meta:
        model = UsuarioInsignia
        load_instance = True
        include = ('fecha_otorgamiento',)
    
    insignia = fields.Nested(InsigniaSchema, dump_only=True)


class UsuarioCompletoSchema(UsuarioSchema):
    """Schema completo para Usuario con relaciones"""
    perfil_investigador = fields.Nested(PerfilInvestigadorSchema, dump_only=True)
    programas = fields.List(fields.Nested(UsuarioProgramaSchema, dump_only=True))
    insignias = fields.List(fields.Nested(UsuarioInsigniaSchema, dump_only=True))
    nivel = fields.Nested(NivelSchema, dump_only=True)


# Schemas para validación de entrada (request body)
class UsuarioRegisterSchema(Schema):
    """Schema para registro de usuario"""
    nombres = fields.Str(required=True, validate=lambda x: len(x) >= 2)
    apellidos = fields.Str(required=True, validate=lambda x: len(x) >= 2)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 8)
    programa_id = fields.Int()


class UsuarioLoginSchema(Schema):
    """Schema para login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UsuarioUpdateSchema(Schema):
    """Schema para actualizar usuario"""
    nombres = fields.Str(validate=lambda x: len(x) >= 2)
    apellidos = fields.Str(validate=lambda x: len(x) >= 2)
    programa_id = fields.Int()


class PerfilInvestigadorUpdateSchema(Schema):
    """Schema para actualizar perfil investigativo"""
    biografia = fields.Str()
    intereses = fields.List(fields.Str())
    orcid = fields.Str()
    cvlac = fields.Str()
