from extensions import db

# Importar todos los modelos para que SQLAlchemy los registre
from .usuarios import (
    Rol, Usuario, PerfilInvestigador, UsuarioPrograma,
    Nivel, Insignia, UsuarioInsignia
)
from .investigacion import (
    Facultad, Programa, LineaInvestigacion, Semillero, SemilleroLinea,
    SemilleroIntegrante, Proyecto, ProyectoIntegrante, AvanceProyecto, Producto
)
from .eventos import (
    Evento, ParticipacionEvento, Convocatoria, PostulacionConvocatoria
)
from .comunidad import (
    CategoriaPublicacion, Evidencia, Publicacion, PublicacionEvidencia,
    Comentario, Reaccion, Compartido, SeguimientoUsuario,
    SeguimientoSemillero, Notificacion
)
from .gamificacion import (
    TipoActividadXP, Logro, LogroEvidencia, MovimientoXP
)

__all__ = [
    # Usuarios
    'Rol', 'Usuario', 'PerfilInvestigador', 'UsuarioPrograma',
    'Nivel', 'Insignia', 'UsuarioInsignia',
    # Investigación
    'Facultad', 'Programa', 'LineaInvestigacion', 'Semillero', 'SemilleroLinea',
    'SemilleroIntegrante', 'Proyecto', 'ProyectoIntegrante', 'AvanceProyecto', 'Producto',
    # Eventos
    'Evento', 'ParticipacionEvento', 'Convocatoria', 'PostulacionConvocatoria',
    # Comunidad
    'CategoriaPublicacion', 'Evidencia', 'Publicacion', 'PublicacionEvidencia',
    'Comentario', 'Reaccion', 'Compartido', 'SeguimientoUsuario',
    'SeguimientoSemillero', 'Notificacion',
    # Gamificación
    'TipoActividadXP', 'Logro', 'LogroEvidencia', 'MovimientoXP',
]
