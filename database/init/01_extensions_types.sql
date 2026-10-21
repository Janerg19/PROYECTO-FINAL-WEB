-- ==========================================
-- 01_extensions_types.sql
-- Extensiones, ENUMs y tablas catálogo
-- ==========================================

-- Extensiones requeridas
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

-- ENUMs para estados y categorías

-- Estado de cuenta de usuario
CREATE TYPE estado_cuenta AS ENUM ('pendiente', 'aprobada', 'rechazada', 'suspendida');

-- Estado de vinculación a semillero
CREATE TYPE estado_vinculacion AS ENUM ('solicitada', 'aprobada', 'rechazada', 'retirada');

-- Rol en semillero
CREATE TYPE rol_semillero AS ENUM ('lider', 'estudiante');

-- Estado de proyecto
CREATE TYPE estado_proyecto AS ENUM ('formulacion', 'en_curso', 'finalizado', 'cancelado');

-- Tipo de producto
CREATE TYPE tipo_producto AS ENUM ('articulo', 'ponencia', 'patente', 'software', 'libro', 'capitulo', 'otro');

-- Estado de convocatoria
CREATE TYPE estado_convocatoria AS ENUM ('borrador', 'publicada', 'cerrada', 'cancelada');

-- Estado de postulación
CREATE TYPE estado_postulacion AS ENUM ('enviada', 'en_revision', 'aprobada', 'rechazada');

-- Tipo de reacción
CREATE TYPE tipo_reaccion AS ENUM ('me_gusta', 'me_encanta', 'me_interesa');

-- Estado de logro
CREATE TYPE estado_logro AS ENUM ('enviado', 'aprobado', 'rechazado');

-- Tipo de actividad para XP
CREATE TYPE tipo_actividad AS ENUM (
    'registro_usuario',
    'vinculacion_semillero',
    'publicacion',
    'comentario',
    'reaccion',
    'proyecto_registrado',
    'producto_registrado',
    'evento_participacion',
    'logro_validado'
);

-- Tablas catálogo (maestras)

-- Roles del sistema
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE rol IS 'Catálogo de roles del sistema (estudiante, docente, admin, visitante)';
COMMENT ON COLUMN rol.nombre IS 'Nombre único del rol';
COMMENT ON COLUMN rol.descripcion IS 'Descripción del rol y sus responsabilidades';

-- Facultades
CREATE TABLE facultad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(20) UNIQUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE facultad IS 'Catálogo de facultades de la universidad';
COMMENT ON COLUMN facultad.codigo IS 'Código institucional de la facultad';

-- Programas académicos
CREATE TABLE programa (
    id SERIAL PRIMARY KEY,
    facultad_id INTEGER NOT NULL REFERENCES facultad(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE,
    tipo VARCHAR(50), -- pregrado, posgrado, etc.
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (facultad_id, nombre)
);

COMMENT ON TABLE programa IS 'Catálogo de programas académicos por facultad';
COMMENT ON COLUMN programa.facultad_id IS 'FK a facultad';
COMMENT ON COLUMN programa.tipo IS 'Tipo de programa (pregrado, posgrado, etc.)';

-- Tipos de actividad con XP base
CREATE TABLE tipo_actividad_xp (
    id SERIAL PRIMARY KEY,
    tipo tipo_actividad NOT NULL UNIQUE,
    xp_base INTEGER NOT NULL CHECK (xp_base > 0),
    descripcion TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE tipo_actividad_xp IS 'Catálogo de tipos de actividad con su XP base';
COMMENT ON COLUMN tipo_actividad_xp.xp_base IS 'XP base otorgada por esta actividad';

-- Niveles con umbrales de XP
CREATE TABLE nivel (
    id SERIAL PRIMARY KEY,
    numero INTEGER NOT NULL UNIQUE CHECK (numero BETWEEN 1 AND 5),
    umbral_xp INTEGER NOT NULL CHECK (umbral_xp > 0),
    estrellas INTEGER NOT NULL CHECK (estrellas BETWEEN 1 AND 5),
    descripcion TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE nivel IS 'Niveles de gamificación con umbrales de XP y estrellas';
COMMENT ON COLUMN nivel.umbral_xp IS 'XP mínima requerida para alcanzar este nivel';

-- Insignias
CREATE TABLE insignia (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    criterio TEXT, -- Regla para otorgar la insignia
    icono VARCHAR(50), -- Clave del icono SVG
    color VARCHAR(20), -- Color CSS
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE insignia IS 'Catálogo de insignias de reconocimiento';
COMMENT ON COLUMN insignia.criterio IS 'Regla o condición para otorgar la insignia';

-- Categorías de publicación
CREATE TABLE categoria_publicacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    color VARCHAR(20), -- Color CSS para chips
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE categoria_publicacion IS 'Categorías para clasificar publicaciones';
COMMENT ON COLUMN categoria_publicacion.color IS 'Color CSS para chips de categoría';
