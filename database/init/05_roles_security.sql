-- ==========================================
-- 05_roles_security.sql
-- Roles de BD y permisos mínimos
-- ==========================================

-- ==========================================
-- CREAR ROLES DE BASE DE DATOS
-- ==========================================

-- Rol de aplicación (para conexión desde Node.js)
-- Permisos mínimos: solo lo necesario para la aplicación
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'riul_app') THEN
        CREATE ROLE riul_app WITH LOGIN PASSWORD 'cambiar_esto_en_produccion' NOSUPERUSER NOCREATEDB NOCREATEROLE;
    END IF;
END
$$;

COMMENT ON ROLE riul_app IS 'Rol de aplicación con permisos mínimos para conectar desde Node.js';

-- Rol de solo lectura para analítica
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'riul_readonly') THEN
        CREATE ROLE riul_readonly WITH LOGIN PASSWORD 'cambiar_esto_en_produccion' NOSUPERUSER NOCREATEDB NOCREATEROLE;
    END IF;
END
$$;

COMMENT ON ROLE riul_readonly IS 'Rol de solo lectura para consultas de analítica';

-- ==========================================
-- PERMISOS PARA riul_app (APLICACIÓN)
-- ==========================================

-- Permisos sobre esquema public
GRANT USAGE ON SCHEMA public TO riul_app;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO riul_app;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO riul_app;
GRANT UPDATE ON ALL TABLES IN SCHEMA public TO riul_app;
GRANT DELETE ON ALL TABLES IN SCHEMA public TO riul_app;

-- Permisos sobre secuencias
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO riul_app;

-- Permisos sobre funciones
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO riul_app;

-- Permisos sobre vistas (las vistas se incluyen en TABLES)
-- Ya está cubierto por el GRANT SELECT ON ALL TABLES

-- Aplicar permisos a objetos futuros (ALTER DEFAULT PRIVILEGES)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO riul_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO riul_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO riul_app;

-- ==========================================
-- PERMISOS PARA riul_readonly (ANALÍTICA)
-- ==========================================

-- Permisos sobre esquema public
GRANT USAGE ON SCHEMA public TO riul_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO riul_readonly;

-- Permisos sobre secuencias (solo SELECT)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO riul_readonly;

-- Permisos sobre funciones (solo SELECT si retornan datos)
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO riul_readonly;

-- Aplicar permisos a objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO riul_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO riul_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO riul_readonly;

-- ==========================================
-- RESTRICCIONES ADICIONALES DE SEGURIDAD
-- ==========================================

-- El rol riul_app NO puede modificar directamente movimiento_xp (ya protegido por trigger)
-- pero aseguramos que no tenga permisos especiales sobre esa tabla
-- (ya está cubierto por el trigger trg_movimiento_xp_inmutable)

-- ==========================================
-- POLÍTICAS DE ROW LEVEL SECURITY (OPCIONAL)
-- ==========================================

-- Habilitar RLS en tablas sensibles si se requiere filtrado por usuario
-- Por ahora, dejamos RLS deshabilitado y controlamos acceso por rol en la API

-- Ejemplo de cómo se habilitaría (comentado por ahora):
-- ALTER TABLE usuario ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY usuario_puede_ver_propio ON usuario FOR SELECT USING (id = current_setting('app.current_user_id')::INTEGER);
-- CREATE POLICY admin_puede_ver_todo ON usuario FOR SELECT USING (EXISTS (SELECT 1 FROM usuario WHERE id = current_setting('app.current_user_id')::INTEGER AND rol_id = (SELECT id FROM rol WHERE nombre = 'administrador')));

-- ==========================================
-- NOTAS DE SEGURIDAD
-- ==========================================

-- 1. Las contraseñas deben venir de variables de entorno en producción
-- 2. El rol riul_app no debe tener SUPERUSER, CREATEDB ni CREATEROLE
-- 3. El rol riul_readonly solo tiene SELECT, no puede modificar datos
-- 4. La lógica de autorización por rol (estudiante, docente, admin) se maneja en la API
-- 5. Las contraseñas de usuario se hashean con bcrypt en la aplicación, no en BD
-- 6. Los datos sensibles (documentos, evidencias) se almacenan en volumen Docker, no en BD
