-- ==========================================
-- 02_schema.sql
-- Tablas, PK, FK, UNIQUE, CHECK, índices
-- ==========================================

-- ==========================================
-- MÓDULO USUARIOS
-- ==========================================

-- Usuarios del sistema
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER NOT NULL REFERENCES rol(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    estado estado_cuenta NOT NULL DEFAULT 'pendiente',
    validado_por INTEGER REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    fecha_validacion TIMESTAMP,
    documento_ruta VARCHAR(255), -- Ruta del documento de validación
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMP -- Borrado lógico
);

COMMENT ON TABLE usuario IS 'Usuarios del sistema con autenticación y validación';
COMMENT ON COLUMN usuario.password_hash IS 'Hash de contraseña con bcrypt';
COMMENT ON COLUMN usuario.estado IS 'Estado de la cuenta (pendiente/aprobada/rechazada/suspendida)';
COMMENT ON COLUMN usuario.validado_por IS 'ID del administrador que validó la cuenta';
COMMENT ON COLUMN usuario.eliminado_en IS 'Timestamp para borrado lógico (NULL si activo)';

-- Índices en usuario
CREATE INDEX idx_usuario_email ON usuario(email);
CREATE INDEX idx_usuario_estado ON usuario(estado);
CREATE INDEX idx_usuario_rol ON usuario(rol_id);
CREATE INDEX idx_usuario_nombre ON usuario(nombres, apellidos);

-- Perfil investigativo del usuario
CREATE TABLE perfil_investigador (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL UNIQUE REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    biografia TEXT,
    intereses TEXT[], -- Array de intereses de investigación
    orcid VARCHAR(50),
    cvlac VARCHAR(255),
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE perfil_investigador IS 'Hoja de vida investigativa del usuario';
COMMENT ON COLUMN perfil_investigador.intereses IS 'Array de intereses de investigación';
COMMENT ON COLUMN perfil_investigador.orcid IS 'Identificador ORCID del investigador';
COMMENT ON COLUMN perfil_investigador.cvlac IS 'Enlace al CvLAC de Colciencias';

-- Índices en perfil_investigador
CREATE INDEX idx_perfil_usuario ON perfil_investigador(usuario_id);

-- Relación usuario-programa (un usuario puede tener múltiples programas a lo largo del tiempo)
CREATE TABLE usuario_programa (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    programa_id INTEGER NOT NULL REFERENCES programa(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    actual BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (usuario_id, programa_id, fecha_inicio)
);

COMMENT ON TABLE usuario_programa IS 'Relación entre usuarios y programas académicos';
COMMENT ON COLUMN usuario_programa.actual IS 'Indica si es el programa actual del usuario';

-- Índices en usuario_programa
CREATE INDEX idx_usuario_programa_usuario ON usuario_programa(usuario_id);
CREATE INDEX idx_usuario_programa_programa ON usuario_programa(programa_id);
CREATE INDEX idx_usuario_programa_actual ON usuario_programa(actual) WHERE actual = TRUE;

-- ==========================================
-- MÓDULO INVESTIGACIÓN
-- ==========================================

-- Líneas de investigación
CREATE TABLE linea_investigacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL UNIQUE,
    descripcion TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE linea_investigacion IS 'Catálogo de líneas de investigación';

-- Semilleros
CREATE TABLE semillero (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    facultad_id INTEGER NOT NULL REFERENCES facultad(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    programa_id INTEGER REFERENCES programa(id) ON DELETE SET NULL ON UPDATE CASCADE,
    lider_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    fecha_creacion DATE NOT NULL DEFAULT CURRENT_DATE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMP
);

COMMENT ON TABLE semillero IS 'Semilleros de investigación';
COMMENT ON COLUMN semillero.lider_id IS 'Docente líder del semillero';
COMMENT ON COLUMN semillero.activo IS 'Indica si el semillero está activo';

-- Índices en semillero
CREATE INDEX idx_semillero_facultad ON semillero(facultad_id);
CREATE INDEX idx_semillero_programa ON semillero(programa_id);
CREATE INDEX idx_semillero_lider ON semillero(lider_id);
CREATE INDEX idx_semillero_activo ON semillero(activo) WHERE activo = TRUE;

-- Relación semillero-línea de investigación (N:M)
CREATE TABLE semillero_linea (
    id SERIAL PRIMARY KEY,
    semillero_id INTEGER NOT NULL REFERENCES semillero(id) ON DELETE CASCADE ON UPDATE CASCADE,
    linea_id INTEGER NOT NULL REFERENCES linea_investigacion(id) ON DELETE CASCADE ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (semillero_id, linea_id)
);

COMMENT ON TABLE semillero_linea IS 'Relación N:M entre semilleros y líneas de investigación';

-- Índices en semillero_linea
CREATE INDEX idx_semillero_linea_semillero ON semillero_linea(semillero_id);
CREATE INDEX idx_semillero_linea_linea ON semillero_linea(linea_id);

-- Integrantes de semillero (N:M con estado)
CREATE TABLE semillero_integrante (
    id SERIAL PRIMARY KEY,
    semillero_id INTEGER NOT NULL REFERENCES semillero(id) ON DELETE CASCADE ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    rol rol_semillero NOT NULL DEFAULT 'estudiante',
    estado estado_vinculacion NOT NULL DEFAULT 'solicitada',
    fecha_solicitud TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_resolucion TIMESTAMP,
    revisado_por INTEGER REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE, -- Docente líder que aprueba/rechaza
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (semillero_id, usuario_id)
);

COMMENT ON TABLE semillero_integrante IS 'Integrantes de semillero con estado de vinculación';
COMMENT ON COLUMN semillero_integrante.rol IS 'Rol en el semillero (lider/estudiante)';
COMMENT ON COLUMN semillero_integrante.estado IS 'Estado de la vinculación (solicitada/aprobada/rechazada/retirada)';
COMMENT ON COLUMN semillero_integrante.revisado_por IS 'Docente líder que aprobó/rechazó la vinculación';

-- Índices en semillero_integrante
CREATE INDEX idx_semillero_integrante_semillero ON semillero_integrante(semillero_id);
CREATE INDEX idx_semillero_integrante_usuario ON semillero_integrante(usuario_id);
CREATE INDEX idx_semillero_integrante_estado ON semillero_integrante(estado);
CREATE INDEX idx_semillero_integrante_aprobados ON semillero_integrante(semillero_id) WHERE estado = 'aprobada';

-- Proyectos de investigación
CREATE TABLE proyecto (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    semillero_id INTEGER NOT NULL REFERENCES semillero(id) ON DELETE CASCADE ON UPDATE CASCADE,
    estado estado_proyecto NOT NULL DEFAULT 'formulacion',
    fecha_inicio DATE,
    fecha_fin DATE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMP
);

COMMENT ON TABLE proyecto IS 'Proyectos de investigación de los semilleros';

-- Índices en proyecto
CREATE INDEX idx_proyecto_semillero ON proyecto(semillero_id);
CREATE INDEX idx_proyecto_estado ON proyecto(estado);

-- Integrantes de proyecto (N:M)
CREATE TABLE proyecto_integrante (
    id SERIAL PRIMARY KEY,
    proyecto_id INTEGER NOT NULL REFERENCES proyecto(id) ON DELETE CASCADE ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    rol VARCHAR(50) DEFAULT 'investigador',
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (proyecto_id, usuario_id)
);

COMMENT ON TABLE proyecto_integrante IS 'Integrantes de un proyecto';

-- Índices en proyecto_integrante
CREATE INDEX idx_proyecto_integrante_proyecto ON proyecto_integrante(proyecto_id);
CREATE INDEX idx_proyecto_integrante_usuario ON proyecto_integrante(usuario_id);

-- Avances de proyecto
CREATE TABLE avance_proyecto (
    id SERIAL PRIMARY KEY,
    proyecto_id INTEGER NOT NULL REFERENCES proyecto(id) ON DELETE CASCADE ON UPDATE CASCADE,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_avance DATE NOT NULL DEFAULT CURRENT_DATE,
    creado_por INTEGER NOT NULL REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE avance_proyecto IS 'Avances cronológicos de un proyecto';

-- Índices en avance_proyecto
CREATE INDEX idx_avance_proyecto ON avance_proyecto(proyecto_id);
CREATE INDEX idx_avance_fecha ON avance_proyecto(fecha_avance);

-- Productos de investigación
CREATE TABLE producto (
    id SERIAL PRIMARY KEY,
    proyecto_id INTEGER REFERENCES proyecto(id) ON DELETE SET NULL ON UPDATE CASCADE,
    titulo VARCHAR(200) NOT NULL,
    tipo tipo_producto NOT NULL,
    descripcion TEXT,
    fecha_publicacion DATE,
    url VARCHAR(500), -- Enlace al producto (artículo, repositorio, etc.)
    creado_por INTEGER NOT NULL REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE producto IS 'Productos de investigación (artículos, ponencias, patentes, etc.)';
COMMENT ON COLUMN producto.proyecto_id IS 'FK opcional al proyecto asociado';

-- Índices en producto
CREATE INDEX idx_producto_proyecto ON producto(proyecto_id);
CREATE INDEX idx_producto_tipo ON producto(tipo);
CREATE INDEX idx_producto_creador ON producto(creado_por);

-- ==========================================
-- MÓDULO EVENTOS Y CONVOCATORIAS
-- ==========================================

-- Eventos académicos
CREATE TABLE evento (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_evento DATE NOT NULL,
    hora VARCHAR(10), -- HH:MM
    lugar VARCHAR(200),
    creado_por INTEGER NOT NULL REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE evento IS 'Eventos académicos (coloquios, talleres, ferias)';

-- Índices en evento
CREATE INDEX idx_evento_fecha ON evento(fecha_evento);
CREATE INDEX idx_evento_creador ON evento(creado_por);

-- Participación en eventos
CREATE TABLE participacion_evento (
    id SERIAL PRIMARY KEY,
    evento_id INTEGER NOT NULL REFERENCES evento(id) ON DELETE CASCADE ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    rol VARCHAR(50) DEFAULT 'asistente', -- asistente, ponente, organizador
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (evento_id, usuario_id)
);

COMMENT ON TABLE participacion_evento IS 'Registro de participación en eventos';

-- Índices en participacion_evento
CREATE INDEX idx_participacion_evento ON participacion_evento(evento_id);
CREATE INDEX idx_participacion_usuario ON participacion_evento(usuario_id);

-- Convocatorias
CREATE TABLE convocatoria (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    estado estado_convocatoria NOT NULL DEFAULT 'borrador',
    fecha_apertura DATE NOT NULL,
    fecha_cierre DATE NOT NULL,
    validado_por INTEGER REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    fecha_validacion TIMESTAMP,
    creado_por INTEGER NOT NULL REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE convocatoria IS 'Convocatorias de financiación y oportunidades';
COMMENT ON COLUMN convocatoria.validado_por IS 'Administrador que validó la convocatoria';

-- Índices en convocatoria
CREATE INDEX idx_convocatoria_estado ON convocatoria(estado);
CREATE INDEX idx_convocatoria_fechas ON convocatoria(fecha_apertura, fecha_cierre);
CREATE INDEX idx_convocatoria_abiertas ON convocatoria(estado) WHERE estado = 'publicada';

-- Postulaciones a convocatorias
CREATE TABLE postulacion_convocatoria (
    id SERIAL PRIMARY KEY,
    convocatoria_id INTEGER NOT NULL REFERENCES convocatoria(id) ON DELETE CASCADE ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    propuesta TEXT,
    estado estado_postulacion NOT NULL DEFAULT 'enviada',
    fecha_postulacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_resolucion TIMESTAMP,
    revisado_por INTEGER REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (convocatoria_id, usuario_id)
);

COMMENT ON TABLE postulacion_convocatoria IS 'Postulaciones de usuarios a convocatorias';

-- Índices en postulacion_convocatoria
CREATE INDEX idx_postulacion_convocatoria ON postulacion_convocatoria(convocatoria_id);
CREATE INDEX idx_postulacion_usuario ON postulacion_convocatoria(usuario_id);
CREATE INDEX idx_postulacion_estado ON postulacion_convocatoria(estado);

-- ==========================================
-- MÓDULO COMUNIDAD
-- ==========================================

-- Publicaciones
CREATE TABLE publicacion (
    id SERIAL PRIMARY KEY,
    categoria_id INTEGER NOT NULL REFERENCES categoria_publicacion(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    semillero_id INTEGER REFERENCES semillero(id) ON DELETE SET NULL ON UPDATE CASCADE, -- Opcional: publicación en nombre del semillero
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMP
);

COMMENT ON TABLE publicacion IS 'Publicaciones del feed social de la comunidad';
COMMENT ON COLUMN publicacion.semillero_id IS 'Opcional: publicación en nombre del semillero';

-- Índices en publicacion
CREATE INDEX idx_publicacion_usuario ON publicacion(usuario_id);
CREATE INDEX idx_publicacion_semillero ON publicacion(semillero_id);
CREATE INDEX idx_publicacion_categoria ON publicacion(categoria_id);
CREATE INDEX idx_publicacion_fecha ON publicacion(creado_en DESC);
CREATE INDEX idx_publicacion_activas ON publicacion(creado_en DESC) WHERE eliminado_en IS NULL;

-- Evidencias (archivos adjuntos)
CREATE TABLE evidencia (
    id SERIAL PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo_mime VARCHAR(100) NOT NULL,
    tamano_bytes BIGINT NOT NULL CHECK (tamano_bytes > 0),
    ruta VARCHAR(500) NOT NULL, -- Ruta en el volumen Docker
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE evidencia IS 'Metadatos de archivos adjuntos (evidencias)';
COMMENT ON COLUMN evidencia.ruta IS 'Ruta del archivo en el volumen Docker';

-- Índices en evidencia
CREATE INDEX idx_evidencia_ruta ON evidencia(ruta);

-- Relación publicación-evidencia (N:M)
CREATE TABLE publicacion_evidencia (
    id SERIAL PRIMARY KEY,
    publicacion_id INTEGER NOT NULL REFERENCES publicacion(id) ON DELETE CASCADE ON UPDATE CASCADE,
    evidencia_id INTEGER NOT NULL REFERENCES evidencia(id) ON DELETE CASCADE ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (publicacion_id, evidencia_id)
);

COMMENT ON TABLE publicacion_evidencia IS 'Relación N:M entre publicaciones y evidencias';

-- Índices en publicacion_evidencia
CREATE INDEX idx_pub_evidencia_publicacion ON publicacion_evidencia(publicacion_id);
CREATE INDEX idx_pub_evidencia_evidencia ON publicacion_evidencia(evidencia_id);



-- Comentarios en publicaciones
CREATE TABLE comentario (
    id SERIAL PRIMARY KEY,
    publicacion_id INTEGER NOT NULL REFERENCES publicacion(id) ON DELETE CASCADE ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    contenido TEXT NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMP
);

COMMENT ON TABLE comentario IS 'Comentarios en publicaciones';

-- Índices en comentario
CREATE INDEX idx_comentario_publicacion ON comentario(publicacion_id);
CREATE INDEX idx_comentario_usuario ON comentario(usuario_id);
CREATE INDEX idx_comentario_fecha ON comentario(creado_en DESC);

-- Reacciones en publicaciones
CREATE TABLE reaccion (
    id SERIAL PRIMARY KEY,
    publicacion_id INTEGER NOT NULL REFERENCES publicacion(id) ON DELETE CASCADE ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    tipo tipo_reaccion NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (publicacion_id, usuario_id, tipo)
);

COMMENT ON TABLE reaccion IS 'Reacciones de usuarios a publicaciones';
COMMENT ON COLUMN reaccion.tipo IS 'Tipo de reacción (me_gusta, me_encanta, me_interesa)';

-- Índices en reaccion
CREATE INDEX idx_reaccion_publicacion ON reaccion(publicacion_id);
CREATE INDEX idx_reaccion_usuario ON reaccion(usuario_id);
CREATE INDEX idx_reaccion_tipo ON reaccion(tipo);

-- Compartidos de publicaciones
CREATE TABLE compartido (
    id SERIAL PRIMARY KEY,
    publicacion_id INTEGER NOT NULL REFERENCES publicacion(id) ON DELETE CASCADE ON UPDATE CASCADE,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (publicacion_id, usuario_id)
);

COMMENT ON TABLE compartido IS 'Registro de cuándo un usuario compartió una publicación';

-- Índices en compartido
CREATE INDEX idx_compartido_publicacion ON compartido(publicacion_id);
CREATE INDEX idx_compartido_usuario ON compartido(usuario_id);

-- Seguimiento (follow) entre usuarios
CREATE TABLE seguimiento_usuario (
    id SERIAL PRIMARY KEY,
    seguidor_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    seguido_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (seguidor_id, seguido_id),
    CHECK (seguidor_id != seguido_id)
);

COMMENT ON TABLE seguimiento_usuario IS 'Seguimiento entre usuarios (social follow)';

-- Índices en seguimiento_usuario
CREATE INDEX idx_seguimiento_seguidor ON seguimiento_usuario(seguidor_id);
CREATE INDEX idx_seguimiento_seguido ON seguimiento_usuario(seguido_id);

-- Seguimiento de semilleros
CREATE TABLE seguimiento_semillero (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    semillero_id INTEGER NOT NULL REFERENCES semillero(id) ON DELETE CASCADE ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (usuario_id, semillero_id)
);

COMMENT ON TABLE seguimiento_semillero IS 'Usuarios que siguen un semillero';

-- Índices en seguimiento_semillero
CREATE INDEX idx_seguimiento_semillero_usuario ON seguimiento_semillero(usuario_id);
CREATE INDEX idx_seguimiento_semillero_semillero ON seguimiento_semillero(semillero_id);

-- Notificaciones
CREATE TABLE notificacion (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    tipo VARCHAR(50) NOT NULL, -- tipo de notificación
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT,
    leida BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_lectura TIMESTAMP,
    referencia_tipo VARCHAR(50), -- Tipo de entidad referenciada (publicacion, logro, vinculacion, etc.)
    referencia_id INTEGER, -- ID de la entidad referenciada
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE notificacion IS 'Notificaciones para usuarios';
COMMENT ON COLUMN notificacion.leida IS 'Indica si el usuario leyó la notificación';
COMMENT ON COLUMN notificacion.referencia_tipo IS 'Tipo de entidad referenciada (opcional)';
COMMENT ON COLUMN notificacion.referencia_id IS 'ID de la entidad referenciada (opcional)';

-- Índices en notificacion
CREATE INDEX idx_notificacion_usuario ON notificacion(usuario_id);
CREATE INDEX idx_notificacion_leida ON notificacion(usuario_id, leida) WHERE leida = FALSE;
CREATE INDEX idx_notificacion_fecha ON notificacion(creado_en DESC);

-- ==========================================
-- MÓDULO GAMIFICACIÓN
-- ==========================================

-- Logros enviados por usuarios
CREATE TABLE logro (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    tipo VARCHAR(100) NOT NULL, -- Tipo de logro (artículo, ponencia, proyecto, patente, etc.)
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    estado estado_logro NOT NULL DEFAULT 'enviado',
    validado_por INTEGER REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE,
    fecha_validacion TIMESTAMP,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE logro IS 'Logros enviados por usuarios para validación';
COMMENT ON COLUMN logro.validado_por IS 'Administrador que validó el logro';

-- Índices en logro
CREATE INDEX idx_logro_usuario ON logro(usuario_id);
CREATE INDEX idx_logro_estado ON logro(estado);
CREATE INDEX idx_logro_pendientes ON logro(estado) WHERE estado = 'enviado';

-- Relación logro-evidencia (N:M)
CREATE TABLE logro_evidencia (
    id SERIAL PRIMARY KEY,
    logro_id INTEGER NOT NULL REFERENCES logro(id) ON DELETE CASCADE ON UPDATE CASCADE,
    evidencia_id INTEGER NOT NULL REFERENCES evidencia(id) ON DELETE CASCADE ON UPDATE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (logro_id, evidencia_id)
);

COMMENT ON TABLE logro_evidencia IS 'Relación N:M entre logros y evidencias';

-- Índices en logro_evidencia
CREATE INDEX idx_logro_evidencia_logro ON logro_evidencia(logro_id);
CREATE INDEX idx_logro_evidencia_evidencia ON logro_evidencia(evidencia_id);

-- Movimientos de XP (historial inmutable)
CREATE TABLE movimiento_xp (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    tipo_actividad_id INTEGER NOT NULL REFERENCES tipo_actividad_xp(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    xp_ganada INTEGER NOT NULL CHECK (xp_ganada > 0),
    referencia_tipo VARCHAR(50), -- Tipo de entidad que generó el XP (logro, publicacion, etc.)
    referencia_id INTEGER, -- ID de la entidad referenciada
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE movimiento_xp IS 'Historial inmutable de movimientos de XP';
COMMENT ON COLUMN movimiento_xp.xp_ganada IS 'XP ganada en este movimiento (inmutable)';

-- Índices en movimiento_xp
CREATE INDEX idx_movimiento_usuario ON movimiento_xp(usuario_id);
CREATE INDEX idx_movimiento_fecha ON movimiento_xp(creado_en DESC);

-- XP total por usuario (mantenido por trigger)
ALTER TABLE usuario ADD COLUMN xp_total INTEGER NOT NULL DEFAULT 0 CHECK (xp_total >= 0);
COMMENT ON COLUMN usuario.xp_total IS 'XP total acumulado del usuario (mantenido por trigger)';

-- Nivel actual por usuario (mantenido por trigger)
ALTER TABLE usuario ADD COLUMN nivel_id INTEGER REFERENCES nivel(id) ON DELETE SET NULL ON UPDATE CASCADE;
COMMENT ON COLUMN usuario.nivel_id IS 'Nivel actual del usuario (mantenido por trigger)';

-- Índice en usuario.xp_total para ranking
CREATE INDEX idx_usuario_xp_total ON usuario(xp_total DESC);

-- Relación usuario-insignia
CREATE TABLE usuario_insignia (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    insignia_id INTEGER NOT NULL REFERENCES insignia(id) ON DELETE CASCADE ON UPDATE CASCADE,
    otorgada_por INTEGER REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE, -- Administrador o sistema
    fecha_otorgamiento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (usuario_id, insignia_id)
);

COMMENT ON TABLE usuario_insignia IS 'Insignias otorgadas a usuarios';
COMMENT ON COLUMN usuario_insignia.otorgada_por IS 'Usuario (admin) o sistema que otorgó la insignia';

-- Índices en usuario_insignia
CREATE INDEX idx_usuario_insignia_usuario ON usuario_insignia(usuario_id);
CREATE INDEX idx_usuario_insignia_insignia ON usuario_insignia(insignia_id);
