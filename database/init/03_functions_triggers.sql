-- ==========================================
-- 03_functions_triggers.sql
-- Lógica de negocio en la base de datos
-- ==========================================

-- ==========================================
-- TRIGGER PARA actualizado_en
-- ==========================================

-- Función genérica para actualizar actualizado_en
CREATE OR REPLACE FUNCTION actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas con actualizado_en
CREATE TRIGGER trg_usuario_actualizar
    BEFORE UPDATE ON usuario
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_perfil_investigador_actualizar
    BEFORE UPDATE ON perfil_investigador
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_semillero_actualizar
    BEFORE UPDATE ON semillero
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_semillero_integrante_actualizar
    BEFORE UPDATE ON semillero_integrante
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_proyecto_actualizar
    BEFORE UPDATE ON proyecto
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_avance_proyecto_actualizar
    BEFORE UPDATE ON avance_proyecto
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_producto_actualizar
    BEFORE UPDATE ON producto
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_evento_actualizar
    BEFORE UPDATE ON evento
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_convocatoria_actualizar
    BEFORE UPDATE ON convocatoria
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_postulacion_convocatoria_actualizar
    BEFORE UPDATE ON postulacion_convocatoria
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_publicacion_actualizar
    BEFORE UPDATE ON publicacion
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_comentario_actualizar
    BEFORE UPDATE ON comentario
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trg_logro_actualizar
    BEFORE UPDATE ON logro
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

-- ==========================================
-- LÓGICA DE GAMIFICACIÓN
-- ==========================================

-- Función para actualizar XP total y nivel de un usuario
CREATE OR REPLACE FUNCTION actualizar_xp_usuario(p_usuario_id INTEGER)
RETURNS VOID AS $$
DECLARE
    v_xp_total INTEGER;
    v_nivel_id INTEGER;
BEGIN
    -- Sumar XP total del usuario
    SELECT COALESCE(SUM(xp_ganada), 0) INTO v_xp_total
    FROM movimiento_xp
    WHERE usuario_id = p_usuario_id;

    -- Actualizar XP total
    UPDATE usuario
    SET xp_total = v_xp_total
    WHERE id = p_usuario_id;

    -- Determinar nivel según umbral de XP
    SELECT id INTO v_nivel_id
    FROM nivel
    WHERE umbral_xp <= v_xp_total
    ORDER BY umbral_xp DESC
    LIMIT 1;

    -- Si no hay nivel suficiente, asignar el más bajo
    IF v_nivel_id IS NULL THEN
        SELECT id INTO v_nivel_id FROM nivel ORDER BY umbral_xp ASC LIMIT 1;
    END IF;

    -- Actualizar nivel
    UPDATE usuario
    SET nivel_id = v_nivel_id
    WHERE id = p_usuario_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION actualizar_xp_usuario IS 'Recalcula XP total y nivel de un usuario';

-- Función para insertar movimiento XP
CREATE OR REPLACE FUNCTION insertar_movimiento_xp(
    p_usuario_id INTEGER,
    p_tipo_actividad tipo_actividad,
    p_referencia_tipo VARCHAR DEFAULT NULL,
    p_referencia_id INTEGER DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_tipo_id INTEGER;
    v_xp_base INTEGER;
    v_movimiento_id INTEGER;
BEGIN
    -- Obtener tipo de actividad y XP base
    SELECT id, xp_base INTO v_tipo_id, v_xp_base
    FROM tipo_actividad_xp
    WHERE tipo = p_tipo_actividad;

    IF v_tipo_id IS NULL THEN
        RAISE EXCEPTION 'Tipo de actividad no encontrado: %', p_tipo_actividad;
    END IF;

    -- Insertar movimiento XP
    INSERT INTO movimiento_xp (usuario_id, tipo_actividad_id, xp_ganada, referencia_tipo, referencia_id)
    VALUES (p_usuario_id, v_tipo_id, v_xp_base, p_referencia_tipo, p_referencia_id)
    RETURNING id INTO v_movimiento_id;

    -- Actualizar XP total y nivel
    PERFORM actualizar_xp_usuario(p_usuario_id);

    RETURN v_movimiento_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION insertar_movimiento_xp IS 'Inserta un movimiento de XP y actualiza el total y nivel del usuario';

-- Trigger para impedir modificaciones en movimiento_xp (inmutable)
CREATE OR REPLACE FUNCTION impedir_modificacion_movimiento_xp()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Los movimientos de XP son inmutables y no pueden modificarse';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_movimiento_xp_inmutable
    BEFORE UPDATE OR DELETE ON movimiento_xp
    FOR EACH ROW
    EXECUTE FUNCTION impedir_modificacion_movimiento_xp();

COMMENT ON TRIGGER trg_movimiento_xp_inmutable ON movimiento_xp IS 'Impide modificaciones en movimiento_xp (historial inmutable)';

-- Función para otorgar insignias según reglas
CREATE OR REPLACE FUNCTION otorgar_insignias_usuario(p_usuario_id INTEGER)
RETURNS VOID AS $$
DECLARE
    v_xp_total INTEGER;
    v_nivel_estrellas INTEGER;
    v_insignia RECORD;
BEGIN
    -- Obtener XP total y estrellas del nivel actual
    SELECT u.xp_total, n.estrellas
    INTO v_xp_total, v_nivel_estrellas
    FROM usuario u
    JOIN nivel n ON u.nivel_id = n.id
    WHERE u.id = p_usuario_id;

    -- Regla 1: Insignia por nivel (nivel 3+)
    IF v_nivel_estrellas >= 3 THEN
        INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por)
        SELECT p_usuario_id, id, NULL
        FROM insignia
        WHERE nombre = 'Nivel 3 alcanzado'
        ON CONFLICT (usuario_id, insignia_id) DO NOTHING;
    END IF;

    -- Regla 2: Insignia por XP acumulado (1000+ XP)
    IF v_xp_total >= 1000 THEN
        INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por)
        SELECT p_usuario_id, id, NULL
        FROM insignia
        WHERE nombre = '1000 XP'
        ON CONFLICT (usuario_id, insignia_id) DO NOTHING;
    END IF;

    -- Regla 3: Insignia por número de logros validados
    DECLARE
        v_num_logros INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_num_logros
        FROM logro
        WHERE usuario_id = p_usuario_id AND estado = 'aprobado';

        IF v_num_logros >= 5 THEN
            INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por)
            SELECT p_usuario_id, id, NULL
            FROM insignia
            WHERE nombre = '5 logros validados'
            ON CONFLICT (usuario_id, insignia_id) DO NOTHING;
        END IF;
    END;

    -- Regla 4: Insignia por publicaciones
    DECLARE
        v_num_publicaciones INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_num_publicaciones
        FROM publicacion
        WHERE usuario_id = p_usuario_id AND eliminado_en IS NULL;

        IF v_num_publicaciones >= 10 THEN
            INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por)
            SELECT p_usuario_id, id, NULL
            FROM insignia
            WHERE nombre = '10 publicaciones'
            ON CONFLICT (usuario_id, insignia_id) DO NOTHING;
        END IF;
    END;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION otorgar_insignias_usuario IS 'Otorga insignias a un usuario según reglas de XP, nivel, logros y publicaciones';

-- Trigger para aprobar logro: insertar XP, actualizar nivel, otorgar insignias, notificar
CREATE OR REPLACE FUNCTION aprobar_logro()
RETURNS TRIGGER AS $$
DECLARE
    v_usuario_id INTEGER;
BEGIN
    -- Solo actuar cuando el estado cambia a 'aprobado'
    IF NEW.estado = 'aprobado' AND OLD.estado != 'aprobado' THEN
        v_usuario_id := NEW.usuario_id;

        -- Validar que el validador sea administrador
        IF EXISTS (SELECT 1 FROM usuario WHERE id = NEW.validado_por AND rol_id = (SELECT id FROM rol WHERE nombre = 'administrador')) THEN
            -- Insertar movimiento XP
            PERFORM insertar_movimiento_xp(v_usuario_id, 'logro_validado', 'logro', NEW.id);

            -- Otorgar insignias
            PERFORM otorgar_insignias_usuario(v_usuario_id);

            -- Crear notificación al usuario
            INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
            VALUES (
                v_usuario_id,
                'logro_aprobado',
                'Logro validado',
                'Tu logro "' || NEW.titulo || '" ha sido validado. ¡Has ganado XP!',
                'logro',
                NEW.id
            );
        ELSE
            RAISE EXCEPTION 'Solo un administrador puede validar logros';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_logro_aprobado
    AFTER UPDATE ON logro
    FOR EACH ROW
    EXECUTE FUNCTION aprobar_logro();

COMMENT ON TRIGGER trg_logro_aprobado ON logro IS 'Al aprobar un logro, inserta XP, actualiza nivel, otorga insignias y notifica';

-- ==========================================
-- LÓGICA DE VINCULACIÓN A SEMILLERO
-- ==========================================

-- Función para solicitar vinculación a semillero
CREATE OR REPLACE FUNCTION solicitar_vinculacion(p_semillero_id INTEGER, p_usuario_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_vinculacion_id INTEGER;
BEGIN
    -- Verificar que el usuario no esté ya vinculado
    IF EXISTS (SELECT 1 FROM semillero_integrante WHERE semillero_id = p_semillero_id AND usuario_id = p_usuario_id) THEN
        RAISE EXCEPTION 'El usuario ya tiene una vinculación con este semillero';
    END IF;

    -- Insertar solicitud
    INSERT INTO semillero_integrante (semillero_id, usuario_id, estado, rol)
    VALUES (p_semillero_id, p_usuario_id, 'solicitada', 'estudiante')
    RETURNING id INTO v_vinculacion_id;

    -- Notificar al docente líder del semillero
    INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
    SELECT
        lider_id,
        'vinculacion_solicitada',
        'Solicitud de vinculación',
        'Un nuevo estudiante ha solicitado vincularse a tu semillero.',
        'semillero_integrante',
        v_vinculacion_id
    FROM semillero
    WHERE id = p_semillero_id;

    RETURN v_vinculacion_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION solicitar_vinculacion IS 'Crea una solicitud de vinculación y notifica al docente líder';

-- Función para resolver vinculación (aprobar/rechazar)
CREATE OR REPLACE FUNCTION resolver_vinculacion(p_vinculacion_id INTEGER, p_resolucion estado_vinculacion, p_revisor_id INTEGER)
RETURNS VOID AS $$
DECLARE
    v_usuario_id INTEGER;
    v_semillero_id INTEGER;
BEGIN
    -- Actualizar estado de vinculación
    UPDATE semillero_integrante
    SET estado = p_resolucion,
        fecha_resolucion = CURRENT_TIMESTAMP,
        revisado_por = p_revisor_id
    WHERE id = p_vinculacion_id;

    -- Obtener datos para notificación
    SELECT usuario_id, semillero_id INTO v_usuario_id, v_semillero_id
    FROM semillero_integrante
    WHERE id = p_vinculacion_id;

    -- Si se aprobó, dar XP por vinculación
    IF p_resolucion = 'aprobada' THEN
        PERFORM insertar_movimiento_xp(v_usuario_id, 'vinculacion_semillero', 'semillero_integrante', p_vinculacion_id);

        -- Notificar al usuario
        INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
        VALUES (
            v_usuario_id,
            'vinculacion_aprobada',
            'Vinculación aprobada',
            'Tu solicitud de vinculación al semillero ha sido aprobada.',
            'semillero_integrante',
            p_vinculacion_id
        );
    ELSE
        -- Notificar rechazo
        INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
        VALUES (
            v_usuario_id,
            'vinculacion_rechazada',
            'Vinculación rechazada',
            'Tu solicitud de vinculación al semillero ha sido rechazada.',
            'semillero_integrante',
            p_vinculacion_id
        );
    END IF;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION resolver_vinculacion IS 'Aprueba o rechaza una vinculación, da XP si se aprueba y notifica';

-- Trigger para impedir doble vinculación al mismo semillero
CREATE OR REPLACE FUNCTION impedir_doble_vinculacion()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM semillero_integrante
        WHERE semillero_id = NEW.semillero_id
        AND usuario_id = NEW.usuario_id
        AND id != NEW.id
    ) THEN
        RAISE EXCEPTION 'El usuario ya está vinculado a este semillero';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_semillero_integrante_unico
    BEFORE INSERT OR UPDATE ON semillero_integrante
    FOR EACH ROW
    EXECUTE FUNCTION impedir_doble_vinculacion();

COMMENT ON TRIGGER trg_semillero_integrante_unico ON semillero_integrante IS 'Impide vincular dos veces al mismo usuario al mismo semillero';

-- ==========================================
-- LÓGICA DE PUBLICACIONES
-- ==========================================

-- Función para registrar publicación
CREATE OR REPLACE FUNCTION registrar_publicacion(
    p_usuario_id INTEGER,
    p_categoria_id INTEGER,
    p_titulo VARCHAR,
    p_contenido TEXT,
    p_semillero_id INTEGER DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_publicacion_id INTEGER;
BEGIN
    -- Insertar publicación
    INSERT INTO publicacion (usuario_id, categoria_id, titulo, contenido, semillero_id)
    VALUES (p_usuario_id, p_categoria_id, p_titulo, p_contenido, p_semillero_id)
    RETURNING id INTO v_publicacion_id;

    -- Dar XP por publicación
    PERFORM insertar_movimiento_xp(p_usuario_id, 'publicacion', 'publicacion', v_publicacion_id);

    -- Notificar a seguidores del usuario
    INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
    SELECT
        seguidor_id,
        'nueva_publicacion',
        'Nueva publicación',
        (SELECT nombres || ' ' || apellidos FROM usuario WHERE id = p_usuario_id) || ' publicó algo nuevo.',
        'publicacion',
        v_publicacion_id
    FROM seguimiento_usuario
    WHERE seguido_id = p_usuario_id;

    RETURN v_publicacion_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION registrar_publicacion IS 'Crea una publicación, da XP y notifica a seguidores';

-- Trigger para impedir doble reacción del mismo tipo
CREATE OR REPLACE FUNCTION impedir_doble_reaccion()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM reaccion
        WHERE publicacion_id = NEW.publicacion_id
        AND usuario_id = NEW.usuario_id
        AND tipo = NEW.tipo
        AND id != NEW.id
    ) THEN
        RAISE EXCEPTION 'El usuario ya reaccionó con este tipo a esta publicación';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reaccion_unico
    BEFORE INSERT OR UPDATE ON reaccion
    FOR EACH ROW
    EXECUTE FUNCTION impedir_doble_reaccion();

COMMENT ON TRIGGER trg_reaccion_unico ON reaccion IS 'Impide reaccionar dos veces con el mismo tipo a la misma publicación';

-- ==========================================
-- LÓGICA DE VALIDACIÓN DE CUENTAS
-- ==========================================

-- Trigger para impedir login con cuenta no aprobada
-- Este trigger se ejecuta en la aplicación, no en BD, pero documentamos la regla

-- Función para validar cuenta
CREATE OR REPLACE FUNCTION validar_cuenta(p_usuario_id INTEGER, p_validador_id INTEGER)
RETURNS VOID AS $$
BEGIN
    -- Actualizar estado de cuenta
    UPDATE usuario
    SET estado = 'aprobada',
        validado_por = p_validador_id,
        fecha_validacion = CURRENT_TIMESTAMP
    WHERE id = p_usuario_id;

    -- Dar XP por registro
    PERFORM insertar_movimiento_xp(p_usuario_id, 'registro_usuario', 'usuario', p_usuario_id);

    -- Notificar al usuario
    INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
    VALUES (
        p_usuario_id,
        'cuenta_validada',
        'Cuenta validada',
        'Tu cuenta institucional ha sido validada. Ya puedes acceder a RIUL.',
        'usuario',
        p_usuario_id
    );
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION validar_cuenta IS 'Valida una cuenta, da XP y notifica al usuario';

-- ==========================================
-- LÓGICA DE CONVOCATORIAS
-- ==========================================

-- Trigger para notificar al publicar convocatoria
CREATE OR REPLACE FUNCTION notificar_convocatoria_publicada()
RETURNS TRIGGER AS $$
BEGIN
    -- Solo actuar cuando el estado cambia a 'publicada'
    IF NEW.estado = 'publicada' AND OLD.estado != 'publicada' THEN
        -- Notificar a todos los usuarios activos
        INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
        SELECT
            id,
            'convocatoria_publicada',
            'Nueva convocatoria',
            'Se ha publicado una nueva convocatoria: ' || NEW.titulo,
            'convocatoria',
            NEW.id
        FROM usuario
        WHERE estado = 'aprobada' AND eliminado_en IS NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_convocatoria_publicada
    AFTER UPDATE ON convocatoria
    FOR EACH ROW
    EXECUTE FUNCTION notificar_convocatoria_publicada();

COMMENT ON TRIGGER trg_convocatoria_publicada ON convocatoria IS 'Notifica a todos los usuarios cuando se publica una convocatoria';

-- ==========================================
-- LÓGICA DE COMENTARIOS
-- ==========================================

-- Función para comentar publicación
CREATE OR REPLACE FUNCTION comentar_publicacion(p_publicacion_id INTEGER, p_usuario_id INTEGER, p_contenido TEXT)
RETURNS INTEGER AS $$
DECLARE
    v_comentario_id INTEGER;
    v_autor_id INTEGER;
BEGIN
    -- Insertar comentario
    INSERT INTO comentario (publicacion_id, usuario_id, contenido)
    VALUES (p_publicacion_id, p_usuario_id, p_contenido)
    RETURNING id INTO v_comentario_id;

    -- Obtener autor de la publicación
    SELECT usuario_id INTO v_autor_id
    FROM publicacion
    WHERE id = p_publicacion_id;

    -- Dar XP por comentario
    PERFORM insertar_movimiento_xp(p_usuario_id, 'comentario', 'comentario', v_comentario_id);

    -- Notificar al autor (si no es el mismo)
    IF v_autor_id != p_usuario_id THEN
        INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
        VALUES (
            v_autor_id,
            'nuevo_comentario',
            'Nuevo comentario',
            'Alguien comentó en tu publicación.',
            'comentario',
            v_comentario_id
        );
    END IF;

    RETURN v_comentario_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION comentar_publicacion IS 'Crea un comentario, da XP y notifica al autor';

-- ==========================================
-- LÓGICA DE REACCIONES
-- ==========================================

-- Función para reaccionar a publicación
CREATE OR REPLACE FUNCTION reaccionar_publicacion(p_publicacion_id INTEGER, p_usuario_id INTEGER, p_tipo tipo_reaccion)
RETURNS INTEGER AS $$
DECLARE
    v_reaccion_id INTEGER;
    v_autor_id INTEGER;
BEGIN
    -- Insertar reacción
    INSERT INTO reaccion (publicacion_id, usuario_id, tipo)
    VALUES (p_publicacion_id, p_usuario_id, p_tipo)
    RETURNING id INTO v_reaccion_id;

    -- Obtener autor de la publicación
    SELECT usuario_id INTO v_autor_id
    FROM publicacion
    WHERE id = p_publicacion_id;

    -- Dar XP por reacción
    PERFORM insertar_movimiento_xp(p_usuario_id, 'reaccion', 'reaccion', v_reaccion_id);

    -- Notificar al autor (si no es el mismo)
    IF v_autor_id != p_usuario_id THEN
        INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id)
        VALUES (
            v_autor_id,
            'nueva_reaccion',
            'Nueva reacción',
            'Alguien reaccionó a tu publicación.',
            'reaccion',
            v_reaccion_id
        );
    END IF;

    RETURN v_reaccion_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION reaccionar_publicacion IS 'Crea una reacción, da XP y notifica al autor';
