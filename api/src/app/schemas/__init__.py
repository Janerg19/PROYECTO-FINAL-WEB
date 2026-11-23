# Importar todos los schemas
from .usuarios import (
    RolSchema, UsuarioSchema, PerfilInvestigadorSchema, UsuarioProgramaSchema,
    NivelSchema, InsigniaSchema, UsuarioInsigniaSchema, UsuarioCompletoSchema,
    UsuarioRegisterSchema, UsuarioLoginSchema, UsuarioUpdateSchema, PerfilInvestigadorUpdateSchema
)
from .investigacion import (
    FacultadSchema, ProgramaSchema, LineaInvestigacionSchema, SemilleroSchema,
    SemilleroLineaSchema, SemilleroIntegranteSchema, ProyectoSchema,
    ProyectoIntegranteSchema, AvanceProyectoSchema, ProductoSchema,
    SemilleroCreateSchema, SemilleroUpdateSchema, VinculacionSchema,
    VinculacionResolucionSchema, ProyectoCreateSchema
)
from .eventos import (
    EventoSchema, ParticipacionEventoSchema, ConvocatoriaSchema,
    PostulacionConvocatoriaSchema, EventoCreateSchema, ConvocatoriaCreateSchema,
    PostulacionCreateSchema, PostulacionResolucionSchema
)
from .comunidad import (
    CategoriaPublicacionSchema, EvidenciaSchema, PublicacionSchema,
    ComentarioSchema, ReaccionSchema, SeguimientoUsuarioSchema,
    SeguimientoSemilleroSchema, NotificacionSchema, PublicacionCreateSchema,
    PublicacionUpdateSchema, ComentarioCreateSchema, ReaccionCreateSchema,
    NotificacionUpdateSchema
)
from .gamificacion import (
    TipoActividadXPSchema, LogroSchema, MovimientoXPSchema, GamificacionMeSchema,
    LogroCreateSchema, LogroResolucionSchema
)

__all__ = [
    # Usuarios
    'RolSchema', 'UsuarioSchema', 'PerfilInvestigadorSchema', 'UsuarioProgramaSchema',
    'NivelSchema', 'InsigniaSchema', 'UsuarioInsigniaSchema', 'UsuarioCompletoSchema',
    'UsuarioRegisterSchema', 'UsuarioLoginSchema', 'UsuarioUpdateSchema', 'PerfilInvestigadorUpdateSchema',
    # Investigación
    'FacultadSchema', 'ProgramaSchema', 'LineaInvestigacionSchema', 'SemilleroSchema',
    'SemilleroLineaSchema', 'SemilleroIntegranteSchema', 'ProyectoSchema',
    'ProyectoIntegranteSchema', 'AvanceProyectoSchema', 'ProductoSchema',
    'SemilleroCreateSchema', 'SemilleroUpdateSchema', 'VinculacionSchema',
    'VinculacionResolucionSchema', 'ProyectoCreateSchema',
    # Eventos
    'EventoSchema', 'ParticipacionEventoSchema', 'ConvocatoriaSchema',
    'PostulacionConvocatoriaSchema', 'EventoCreateSchema', 'ConvocatoriaCreateSchema',
    'PostulacionCreateSchema', 'PostulacionResolucionSchema',
    # Comunidad
    'CategoriaPublicacionSchema', 'EvidenciaSchema', 'PublicacionSchema',
    'ComentarioSchema', 'ReaccionSchema', 'SeguimientoUsuarioSchema',
    'SeguimientoSemilleroSchema', 'NotificacionSchema', 'PublicacionCreateSchema',
    'PublicacionUpdateSchema', 'ComentarioCreateSchema', 'ReaccionCreateSchema',
    'NotificacionUpdateSchema',
    # Gamificación
    'TipoActividadXPSchema', 'LogroSchema', 'MovimientoXPSchema', 'GamificacionMeSchema',
    'LogroCreateSchema', 'LogroResolucionSchema',
]
