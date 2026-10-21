# Diccionario de Datos - RIUL

Este documento describe cada tabla, sus atributos, tipos, restricciones y descripciones.

## Tabla de Contenidos

- [Módulo Usuarios](#módulo-usuarios)
- [Módulo Investigación](#módulo-investigación)
- [Módulo Eventos y Convocatorias](#módulo-eventos-y-convocatorias)
- [Módulo Comunidad](#módulo-comunidad)
- [Módulo Gamificación](#módulo-gamificación)

---

## MÓDULO USUARIOS

### rol

Catálogo de roles del sistema (estudiante, docente, admin, visitante).

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del rol |
| nombre | VARCHAR(50) | NOT NULL, UNIQUE | Nombre único del rol (estudiante, docente, administrador, visitante) |
| descripcion | TEXT | - | Descripción del rol y sus responsabilidades |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

### facultad

Catálogo de facultades de la universidad.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la facultad |
| nombre | VARCHAR(100) | NOT NULL, UNIQUE | Nombre de la facultad |
| codigo | VARCHAR(20) | UNIQUE | Código institucional de la facultad |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

### programa

Catálogo de programas académicos por facultad.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del programa |
| facultad_id | INTEGER | NOT NULL, FK → facultad(id), ON DELETE RESTRICT | FK a facultad |
| nombre | VARCHAR(100) | NOT NULL | Nombre del programa académico |
| codigo | VARCHAR(20) | UNIQUE | Código institucional del programa |
| tipo | VARCHAR(50) | - | Tipo de programa (pregrado, posgrado, etc.) |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_usuario_programa_usuario`, `idx_usuario_programa_programa`, `idx_usuario_programa_actual`

### usuario

Usuarios del sistema con autenticación y validación.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del usuario |
| rol_id | INTEGER | NOT NULL, FK → rol(id), ON DELETE RESTRICT | FK a rol |
| nombres | VARCHAR(100) | NOT NULL | Nombres del usuario |
| apellidos | VARCHAR(100) | NOT NULL | Apellidos del usuario |
| email | VARCHAR(255) | NOT NULL, UNIQUE | Correo electrónico único |
| password_hash | VARCHAR(255) | NOT NULL | Hash de contraseña con bcrypt |
| estado | estado_cuenta | NOT NULL, DEFAULT 'pendiente' | Estado de la cuenta (pendiente/aprobada/rechazada/suspendida) |
| validado_por | INTEGER | FK → usuario(id), ON DELETE SET NULL | ID del administrador que validó la cuenta |
| fecha_validacion | TIMESTAMP | - | Fecha de validación de la cuenta |
| documento_ruta | VARCHAR(255) | - | Ruta del documento de validación |
| xp_total | INTEGER | NOT NULL, DEFAULT 0, CHECK (xp_total >= 0) | XP total acumulado del usuario (mantenido por trigger) |
| nivel_id | INTEGER | FK → nivel(id), ON DELETE SET NULL | Nivel actual del usuario (mantenido por trigger) |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |
| eliminado_en | TIMESTAMP | - | Timestamp para borrado lógico (NULL si activo) |

**Índices**: `idx_usuario_email`, `idx_usuario_estado`, `idx_usuario_rol`, `idx_usuario_nombre`, `idx_usuario_xp_total`

### perfil_investigador

Hoja de vida investigativa del usuario.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del perfil |
| usuario_id | INTEGER | NOT NULL, UNIQUE, FK → usuario(id), ON DELETE CASCADE | FK a usuario (1:1) |
| biografia | TEXT | - | Biografía del investigador |
| intereses | TEXT[] | - | Array de intereses de investigación |
| orcid | VARCHAR(50) | - | Identificador ORCID del investigador |
| cvlac | VARCHAR(255) | - | Enlace al CvLAC de Colciencias |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_perfil_usuario`

### usuario_programa

Relación entre usuarios y programas académicos.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la relación |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| programa_id | INTEGER | NOT NULL, FK → programa(id), ON DELETE RESTRICT | FK a programa |
| fecha_inicio | DATE | NOT NULL | Fecha de inicio en el programa |
| fecha_fin | DATE | - | Fecha de fin en el programa |
| actual | BOOLEAN | NOT NULL, DEFAULT TRUE | Indica si es el programa actual del usuario |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_usuario_programa_usuario`, `idx_usuario_programa_programa`, `idx_usuario_programa_actual`

---

## MÓDULO INVESTIGACIÓN

### linea_investigacion

Catálogo de líneas de investigación.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la línea |
| nombre | VARCHAR(150) | NOT NULL, UNIQUE | Nombre de la línea de investigación |
| descripcion | TEXT | - | Descripción de la línea |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

### semillero

Semilleros de investigación.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del semillero |
| nombre | VARCHAR(150) | NOT NULL | Nombre del semillero |
| descripcion | TEXT | - | Descripción del semillero |
| facultad_id | INTEGER | NOT NULL, FK → facultad(id), ON DELETE RESTRICT | FK a facultad |
| programa_id | INTEGER | FK → programa(id), ON DELETE SET NULL | FK opcional a programa |
| lider_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE RESTRICT | Docente líder del semillero |
| fecha_creacion | DATE | NOT NULL, DEFAULT CURRENT_DATE | Fecha de creación del semillero |
| activo | BOOLEAN | NOT NULL, DEFAULT TRUE | Indica si el semillero está activo |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |
| eliminado_en | TIMESTAMP | - | Timestamp para borrado lógico |

**Índices**: `idx_semillero_facultad`, `idx_semillero_programa`, `idx_semillero_lider`, `idx_semillero_activo`

### semillero_linea

Relación N:M entre semilleros y líneas de investigación.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la relación |
| semillero_id | INTEGER | NOT NULL, FK → semillero(id), ON DELETE CASCADE | FK a semillero |
| linea_id | INTEGER | NOT NULL, FK → linea_investigacion(id), ON DELETE CASCADE | FK a línea de investigación |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_semillero_linea_semillero`, `idx_semillero_linea_linea`

### semillero_integrante

Integrantes de semillero con estado de vinculación.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la vinculación |
| semillero_id | INTEGER | NOT NULL, FK → semillero(id), ON DELETE CASCADE | FK a semillero |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| rol | rol_semillero | NOT NULL, DEFAULT 'estudiante' | Rol en el semillero (lider/estudiante) |
| estado | estado_vinculacion | NOT NULL, DEFAULT 'solicitada' | Estado de la vinculación (solicitada/aprobada/rechazada/retirada) |
| fecha_solicitud | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de solicitud de vinculación |
| fecha_resolucion | TIMESTAMP | - | Fecha de resolución (aprobación/rechazo) |
| revisado_por | INTEGER | FK → usuario(id), ON DELETE SET NULL | Docente líder que aprobó/rechazó |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_semillero_integrante_semillero`, `idx_semillero_integrante_usuario`, `idx_semillero_integrante_estado`, `idx_semillero_integrante_aprobados`

### proyecto

Proyectos de investigación de los semilleros.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del proyecto |
| titulo | VARCHAR(200) | NOT NULL | Título del proyecto |
| descripcion | TEXT | - | Descripción del proyecto |
| semillero_id | INTEGER | NOT NULL, FK → semillero(id), ON DELETE CASCADE | FK a semillero |
| estado | estado_proyecto | NOT NULL, DEFAULT 'formulacion' | Estado del proyecto (formulacion/en_curso/finalizado/cancelado) |
| fecha_inicio | DATE | - | Fecha de inicio del proyecto |
| fecha_fin | DATE | - | Fecha de fin del proyecto |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |
| eliminado_en | TIMESTAMP | - | Timestamp para borrado lógico |

**Índices**: `idx_proyecto_semillero`, `idx_proyecto_estado`

### proyecto_integrante

Integrantes de un proyecto.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la participación |
| proyecto_id | INTEGER | NOT NULL, FK → proyecto(id), ON DELETE CASCADE | FK a proyecto |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| rol | VARCHAR(50) | DEFAULT 'investigador' | Rol en el proyecto |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_proyecto_integrante_proyecto`, `idx_proyecto_integrante_usuario`

### avance_proyecto

Avances cronológicos de un proyecto.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del avance |
| proyecto_id | INTEGER | NOT NULL, FK → proyecto(id), ON DELETE CASCADE | FK a proyecto |
| titulo | VARCHAR(200) | NOT NULL | Título del avance |
| descripcion | TEXT | - | Descripción del avance |
| fecha_avance | DATE | NOT NULL, DEFAULT CURRENT_DATE | Fecha del avance |
| creado_por | INTEGER | NOT NULL, FK → usuario(id), ON DELETE SET NULL | Usuario que creó el avance |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_avance_proyecto`, `idx_avance_fecha`

### producto

Productos de investigación (artículos, ponencias, patentes, etc.).

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del producto |
| proyecto_id | INTEGER | FK → proyecto(id), ON DELETE SET NULL | FK opcional al proyecto asociado |
| titulo | VARCHAR(200) | NOT NULL | Título del producto |
| tipo | tipo_producto | NOT NULL | Tipo de producto (articulo/ponencia/patente/software/libro/capitulo/otro) |
| descripcion | TEXT | - | Descripción del producto |
| fecha_publicacion | DATE | - | Fecha de publicación |
| url | VARCHAR(500) | - | Enlace al producto (artículo, repositorio, etc.) |
| creado_por | INTEGER | NOT NULL, FK → usuario(id), ON DELETE SET NULL | Usuario que creó el producto |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_producto_proyecto`, `idx_producto_tipo`, `idx_producto_creador`

---

## MÓDULO EVENTOS Y CONVOCATORIAS

### evento

Eventos académicos (coloquios, talleres, ferias).

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del evento |
| titulo | VARCHAR(200) | NOT NULL | Título del evento |
| descripcion | TEXT | - | Descripción del evento |
| fecha_evento | DATE | NOT NULL | Fecha del evento |
| hora | VARCHAR(10) | - | Hora del evento (HH:MM) |
| lugar | VARCHAR(200) | - | Lugar del evento |
| creado_por | INTEGER | NOT NULL, FK → usuario(id), ON DELETE SET NULL | Usuario que creó el evento |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_evento_fecha`, `idx_evento_creador`

### participacion_evento

Registro de participación en eventos.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la participación |
| evento_id | INTEGER | NOT NULL, FK → evento(id), ON DELETE CASCADE | FK a evento |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| rol | VARCHAR(50) | DEFAULT 'asistente' | Rol en el evento (asistente/ponente/organizador) |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_participacion_evento`, `idx_participacion_usuario`

### convocatoria

Convocatorias de financiación y oportunidades.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la convocatoria |
| titulo | VARCHAR(200) | NOT NULL | Título de la convocatoria |
| descripcion | TEXT | - | Descripción de la convocatoria |
| estado | estado_convocatoria | NOT NULL, DEFAULT 'borrador' | Estado (borrador/publicada/cerrada/cancelada) |
| fecha_apertura | DATE | NOT NULL | Fecha de apertura |
| fecha_cierre | DATE | NOT NULL | Fecha de cierre |
| validado_por | INTEGER | FK → usuario(id), ON DELETE SET NULL | Administrador que validó la convocatoria |
| fecha_validacion | TIMESTAMP | - | Fecha de validación |
| creado_por | INTEGER | NOT NULL, FK → usuario(id), ON DELETE SET NULL | Usuario que creó la convocatoria |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_convocatoria_estado`, `idx_convocatoria_fechas`, `idx_convocatoria_abiertas`

### postulacion_convocatoria

Postulaciones de usuarios a convocatorias.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la postulación |
| convocatoria_id | INTEGER | NOT NULL, FK → convocatoria(id), ON DELETE CASCADE | FK a convocatoria |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| propuesta | TEXT | - | Propuesta de postulación |
| estado | estado_postulacion | NOT NULL, DEFAULT 'enviada' | Estado (enviada/en_revision/aprobada/rechazada) |
| fecha_postulacion | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de postulación |
| fecha_resolucion | TIMESTAMP | - | Fecha de resolución |
| revisado_por | INTEGER | FK → usuario(id), ON DELETE SET NULL | Usuario que revisó la postulación |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_postulacion_convocatoria`, `idx_postulacion_usuario`, `idx_postulacion_estado`

---

## MÓDULO COMUNIDAD

### categoria_publicacion

Categorías para clasificar publicaciones.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la categoría |
| nombre | VARCHAR(50) | NOT NULL, UNIQUE | Nombre de la categoría |
| descripcion | TEXT | - | Descripción de la categoría |
| color | VARCHAR(20) | - | Color CSS para chips de categoría |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

### publicacion

Publicaciones del feed social de la comunidad.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la publicación |
| categoria_id | INTEGER | NOT NULL, FK → categoria_publicacion(id), ON DELETE RESTRICT | FK a categoría |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario (autor) |
| semillero_id | INTEGER | FK → semillero(id), ON DELETE SET NULL | FK opcional a semillero (publicación en nombre del semillero) |
| titulo | VARCHAR(200) | NOT NULL | Título de la publicación |
| contenido | TEXT | NOT NULL | Contenido de la publicación |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |
| eliminado_en | TIMESTAMP | - | Timestamp para borrado lógico |

**Índices**: `idx_publicacion_usuario`, `idx_publicacion_semillero`, `idx_publicacion_categoria`, `idx_publicacion_fecha`, `idx_publicacion_activas`

### evidencia

Metadatos de archivos adjuntos (evidencias).

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la evidencia |
| nombre_archivo | VARCHAR(255) | NOT NULL | Nombre original del archivo |
| tipo_mime | VARCHAR(100) | NOT NULL | Tipo MIME del archivo |
| tamano_bytes | BIGINT | NOT NULL, CHECK (tamano_bytes > 0) | Tamaño del archivo en bytes |
| ruta | VARCHAR(500) | NOT NULL | Ruta del archivo en el volumen Docker |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_evidencia_ruta`

### publicacion_evidencia

Relación N:M entre publicaciones y evidencias.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la relación |
| publicacion_id | INTEGER | NOT NULL, FK → publicacion(id), ON DELETE CASCADE | FK a publicación |
| evidencia_id | INTEGER | NOT NULL, FK → evidencia(id), ON DELETE CASCADE | FK a evidencia |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_pub_evidencia_publicacion`, `idx_pub_evidencia_evidencia`

### logro_evidencia

Relación N:M entre logros y evidencias.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la relación |
| logro_id | INTEGER | NOT NULL, FK → logro(id), ON DELETE CASCADE | FK a logro |
| evidencia_id | INTEGER | NOT NULL, FK → evidencia(id), ON DELETE CASCADE | FK a evidencia |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

**Índices**: `idx_logro_evidencia_logro`, `idx_logro_evidencia_evidencia`

### comentario

Comentarios en publicaciones.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del comentario |
| publicacion_id | INTEGER | NOT NULL, FK → publicacion(id), ON DELETE CASCADE | FK a publicación |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario (autor del comentario) |
| contenido | TEXT | NOT NULL | Contenido del comentario |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |
| eliminado_en | TIMESTAMP | - | Timestamp para borrado lógico |

**Índices**: `idx_comentario_publicacion`, `idx_comentario_usuario`, `idx_comentario_fecha`

### reaccion

Reacciones de usuarios a publicaciones.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la reacción |
| publicacion_id | INTEGER | NOT NULL, FK → publicacion(id), ON DELETE CASCADE | FK a publicación |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| tipo | tipo_reaccion | NOT NULL | Tipo de reacción (me_gusta/me_encanta/me_interesa) |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**Índices**: `idx_reaccion_publicacion`, `idx_reaccion_usuario`, `idx_reaccion_tipo`

### compartido

Registro de cuándo un usuario compartió una publicación.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del compartido |
| publicacion_id | INTEGER | NOT NULL, FK → publicacion(id), ON DELETE CASCADE | FK a publicación |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**Índices**: `idx_compartido_publicacion`, `idx_compartido_usuario`

### seguimiento_usuario

Seguimiento entre usuarios (social follow).

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del seguimiento |
| seguidor_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario que sigue |
| seguido_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario seguido |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**Índices**: `idx_seguimiento_seguidor`, `idx_seguimiento_seguido`

### seguimiento_semillero

Usuarios que siguen un semillero.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del seguimiento |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| semillero_id | INTEGER | NOT NULL, FK → semillero(id), ON DELETE CASCADE | FK a semillero |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**Índices**: `idx_seguimiento_semillero_usuario`, `idx_seguimiento_semillero_semillero`

### notificacion

Notificaciones para usuarios.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la notificación |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario destinatario |
| tipo | VARCHAR(50) | NOT NULL | Tipo de notificación |
| titulo | VARCHAR(200) | NOT NULL | Título de la notificación |
| mensaje | TEXT | - | Mensaje de la notificación |
| leida | BOOLEAN | NOT NULL, DEFAULT FALSE | Indica si el usuario leyó la notificación |
| fecha_lectura | TIMESTAMP | - | Fecha de lectura |
| referencia_tipo | VARCHAR(50) | - | Tipo de entidad referenciada (opcional) |
| referencia_id | INTEGER | - | ID de la entidad referenciada (opcional) |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**Índices**: `idx_notificacion_usuario`, `idx_notificacion_leida`, `idx_notificacion_fecha`

---

## MÓDULO GAMIFICACIÓN

### tipo_actividad_xp

Catálogo de tipos de actividad con su XP base.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del tipo |
| tipo | tipo_actividad | NOT NULL, UNIQUE | Tipo de actividad (registro_usuario/vinculacion_semillero/publicacion/etc.) |
| xp_base | INTEGER | NOT NULL, CHECK (xp_base > 0) | XP base otorgada por esta actividad |
| descripcion | TEXT | - | Descripción de la actividad |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

### movimiento_xp

Historial inmutable de movimientos de XP.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del movimiento |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| tipo_actividad_id | INTEGER | NOT NULL, FK → tipo_actividad_xp(id), ON DELETE RESTRICT | FK a tipo de actividad |
| xp_ganada | INTEGER | NOT NULL, CHECK (xp_ganada > 0) | XP ganada en este movimiento (inmutable) |
| referencia_tipo | VARCHAR(50) | - | Tipo de entidad que generó el XP (opcional) |
| referencia_id | INTEGER | - | ID de la entidad referenciada (opcional) |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

**Índices**: `idx_movimiento_usuario`, `idx_movimiento_fecha`

**Triggers**: `trg_movimiento_xp_inmutable` (impide modificaciones/eliminaciones)

### nivel

Niveles de gamificación con umbrales de XP y estrellas.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del nivel |
| numero | INTEGER | NOT NULL, UNIQUE, CHECK (numero BETWEEN 1 AND 5) | Número del nivel (1-5) |
| umbral_xp | INTEGER | NOT NULL, CHECK (umbral_xp > 0) | XP mínima requerida para alcanzar este nivel |
| estrellas | INTEGER | NOT NULL, CHECK (estrellas BETWEEN 1 AND 5) | Estrellas del nivel (1-5) |
| descripcion | TEXT | - | Descripción del nivel |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

### logro

Logros enviados por usuarios para validación.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único del logro |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| tipo | VARCHAR(100) | NOT NULL | Tipo de logro (artículo/ponencia/proyecto/patente/etc.) |
| titulo | VARCHAR(200) | NOT NULL | Título del logro |
| descripcion | TEXT | - | Descripción del logro |
| estado | estado_logro | NOT NULL, DEFAULT 'enviado' | Estado (enviado/aprobado/rechazado) |
| validado_por | INTEGER | FK → usuario(id), ON DELETE SET NULL | Administrador que validó el logro |
| fecha_validacion | TIMESTAMP | - | Fecha de validación |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| actualizado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización (trigger) |

**Índices**: `idx_logro_usuario`, `idx_logro_estado`, `idx_logro_pendientes`

**Triggers**: `trg_logro_aprobado` (al aprobar, inserta XP, actualiza nivel, otorga insignias, notifica)

### insignia

Catálogo de insignias de reconocimiento.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la insignia |
| nombre | VARCHAR(100) | NOT NULL, UNIQUE | Nombre de la insignia |
| descripcion | TEXT | - | Descripción de la insignia |
| criterio | TEXT | - | Regla para otorgar la insignia |
| icono | VARCHAR(50) | - | Clave del icono SVG |
| color | VARCHAR(20) | - | Color CSS |
| creado_en | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

### usuario_insignia

Insignias otorgadas a usuarios.

| Atributo | Tipo | Restricciones | Descripción |
|----------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único de la otorgación |
| usuario_id | INTEGER | NOT NULL, FK → usuario(id), ON DELETE CASCADE | FK a usuario |
| insignia_id | INTEGER | NOT NULL, FK → insignia(id), ON DELETE CASCADE | FK a insignia |
| otorgada_por | INTEGER | FK → usuario(id), ON DELETE SET NULL | Usuario (admin) o sistema que otorgó la insignia |
| fecha_otorgamiento | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Fecha de otorgamiento |

**Índices**: `idx_usuario_insignia_usuario`, `idx_usuario_insignia_insignia`

---

## ENUMs

### estado_cuenta
- `pendiente`
- `aprobada`
- `rechazada`
- `suspendida`

### estado_vinculacion
- `solicitada`
- `aprobada`
- `rechazada`
- `retirada`

### rol_semillero
- `lider`
- `estudiante`

### estado_proyecto
- `formulacion`
- `en_curso`
- `finalizado`
- `cancelado`

### tipo_producto
- `articulo`
- `ponencia`
- `patente`
- `software`
- `libro`
- `capitulo`
- `otro`

### estado_convocatoria
- `borrador`
- `publicada`
- `cerrada`
- `cancelada`

### estado_postulacion
- `enviada`
- `en_revision`
- `aprobada`
- `rechazada`

### tipo_reaccion
- `me_gusta`
- `me_encanta`
- `me_interesa`

### estado_logro
- `enviado`
- `aprobado`
- `rechazado`

### tipo_actividad
- `registro_usuario`
- `vinculacion_semillero`
- `publicacion`
- `comentario`
- `reaccion`
- `proyecto_registrado`
- `producto_registrado`
- `evento_participacion`
- `logro_validado`
