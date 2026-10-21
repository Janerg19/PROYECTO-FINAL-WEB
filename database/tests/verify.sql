-- ==========================================
-- verify.sql
-- Consultas que prueban restricciones, triggers y vistas
-- ==========================================

-- Este script ejecuta pruebas para verificar:
-- 1. Restricciones de integridad (PK, FK, UNIQUE, CHECK)
-- 2. Triggers de lógica de negocio
-- 3. Vistas de analítica y ranking
-- 4. Funciones de gamificación

-- ==========================================
-- PRUEBA 1: RESTRICCIONES DE INTEGRIDAD
-- ==========================================

-- 1.1 Verificar PK y FK
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 1.1: PK y FK ===';

    -- Verificar que existe PK en usuario
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'usuario_pkey') THEN
        RAISE NOTICE '✓ PK en usuario existe';
    ELSE
        RAISE NOTICE '✗ PK en usuario NO existe';
    END IF;

    -- Verificar FK en perfil_investigador
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'perfil_investigador_usuario_id_fkey') THEN
        RAISE NOTICE '✓ FK en perfil_investigador existe';
    ELSE
        RAISE NOTICE '✗ FK en perfil_investigador NO existe';
    END IF;

    -- Verificar UNIQUE en usuario.email
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'usuario_email_key') THEN
        RAISE NOTICE '✓ UNIQUE en usuario.email existe';
    ELSE
        RAISE NOTICE '✗ UNIQUE en usuario.email NO existe';
    END IF;
END
$$;

-- 1.2 Verificar CHECK constraints
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 1.2: CHECK constraints ===';

    -- Intentar insertar XP negativa (debe fallar)
    BEGIN
        INSERT INTO usuario (rol_id, nombres, apellidos, email, password_hash, estado, xp_total, nivel_id)
        VALUES (1, 'Test', 'User', 'test@bad.com', 'hash', 'aprobada', -100, 1);
        RAISE NOTICE '✗ CHECK xp_total >= 0 NO funciona (se insertó XP negativa)';
    EXCEPTION WHEN check_violation THEN
        RAISE NOTICE '✓ CHECK xp_total >= 0 funciona (rechazó XP negativa)';
    END;

    -- Intentar insertar nivel fuera de rango (debe fallar)
    BEGIN
        INSERT INTO nivel (numero, umbral_xp, estrellas)
        VALUES (6, 5000, 6);
        RAISE NOTICE '✗ CHECK nivel/estrellas NO funciona (se insertó nivel 6)';
    EXCEPTION WHEN check_violation THEN
        RAISE NOTICE '✓ CHECK nivel/estrellas funciona (rechazó nivel 6)';
    END;
END
$$;

-- 1.3 Verificar UNIQUE en reaccion (usuario+publicacion+tipo)
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 1.3: UNIQUE en reaccion ===';

    -- Intentar insertar reacción duplicada (debe fallar)
    BEGIN
        INSERT INTO reaccion (publicacion_id, usuario_id, tipo)
        VALUES (1, 6, 'me_gusta'); -- Ya existe en seed
        RAISE NOTICE '✗ UNIQUE en reaccion NO funciona (se insertó duplicado)';
    EXCEPTION WHEN unique_violation THEN
        RAISE NOTICE '✓ UNIQUE en reaccion funciona (rechazó duplicado)';
    END;
END
$$;

-- 1.4 Verificar UNIQUE en semillero_integrante (semillero+usuario)
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 1.4: UNIQUE en semillero_integrante ===';

    -- Intentar insertar vinculación duplicada (debe fallar)
    BEGIN
        INSERT INTO semillero_integrante (semillero_id, usuario_id, rol, estado)
        VALUES (1, 5, 'estudiante', 'solicitada'); -- Ya existe en seed
        RAISE NOTICE '✗ UNIQUE en semillero_integrante NO funciona (se insertó duplicado)';
    EXCEPTION WHEN unique_violation THEN
        RAISE NOTICE '✓ UNIQUE en semillero_integrante funciona (rechazó duplicado)';
    END;
END
$$;

-- ==========================================
-- PRUEBA 2: TRIGGERS DE LÓGICA DE NEGOCIO
-- ==========================================

-- 2.1 Verificar trigger de actualizado_en
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 2.1: Trigger actualizado_en ===';

    -- Guardar timestamp actual
    DECLARE
        v_usuario_id INTEGER := 5;
        v_antes TIMESTAMP;
        v_despues TIMESTAMP;
    BEGIN
        SELECT actualizado_en INTO v_antes FROM usuario WHERE id = v_usuario_id;

        -- Actualizar usuario
        UPDATE usuario SET nombres = 'Juliana' WHERE id = v_usuario_id;

        -- Verificar que cambió
        SELECT actualizado_en INTO v_despues FROM usuario WHERE id = v_usuario_id;

        IF v_despues > v_antes THEN
            RAISE NOTICE '✓ Trigger actualizado_en funciona (timestamp se actualizó)';
        ELSE
            RAISE NOTICE '✗ Trigger actualizado_en NO funciona (timestamp NO se actualizó)';
        END IF;
    END;
END
$$;

-- 2.2 Verificar trigger movimiento_xp inmutable
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 2.2: Trigger movimiento_xp inmutable ===';

    -- Intentar modificar movimiento_xp (debe fallar)
    BEGIN
        UPDATE movimiento_xp SET xp_ganada = 999 WHERE id = 1;
        RAISE NOTICE '✗ Trigger movimiento_xp inmutable NO funciona (se permitió modificación)';
    EXCEPTION WHEN others THEN
        RAISE NOTICE '✓ Trigger movimiento_xp inmutable funciona (rechazó modificación)';
    END;

    -- Intentar eliminar movimiento_xp (debe fallar)
    BEGIN
        DELETE FROM movimiento_xp WHERE id = 1;
        RAISE NOTICE '✗ Trigger movimiento_xp inmutable NO funciona (se permitió eliminación)';
    EXCEPTION WHEN others THEN
        RAISE NOTICE '✓ Trigger movimiento_xp inmutable funciona (rechazó eliminación)';
    END;
END
$$;

-- 2.3 Verificar función insertar_movimiento_xp
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 2.3: Función insertar_movimiento_xp ===';

    DECLARE
        v_usuario_id INTEGER := 5;
        v_xp_antes INTEGER;
        v_xp_despues INTEGER;
        v_movimiento_id INTEGER;
    BEGIN
        -- Obtener XP antes
        SELECT xp_total INTO v_xp_antes FROM usuario WHERE id = v_usuario_id;

        -- Insertar movimiento XP
        SELECT insertar_movimiento_xp(v_usuario_id, 'publicacion', 'publicacion', NULL) INTO v_movimiento_id;

        -- Obtener XP después
        SELECT xp_total INTO v_xp_despues FROM usuario WHERE id = v_usuario_id;

        IF v_xp_despues = v_xp_antes + 80 THEN -- XP base de publicación
            RAISE NOTICE '✓ Función insertar_movimiento_xp funciona (XP incrementó correctamente)';
        ELSE
            RAISE NOTICE '✗ Función insertar_movimiento_xp NO funciona (XP NO incrementó correctamente)';
        END IF;

        -- Limpiar: eliminar el movimiento de prueba
        DELETE FROM movimiento_xp WHERE id = v_movimiento_id;
        UPDATE usuario SET xp_total = v_xp_antes WHERE id = v_usuario_id;
    END;
END
$$;

-- 2.4 Verificar función actualizar_xp_usuario
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 2.4: Función actualizar_xp_usuario ===';

    DECLARE
        v_usuario_id INTEGER := 5;
        v_xp_manual INTEGER;
        v_nivel_antes INTEGER;
        v_nivel_despues INTEGER;
    BEGIN
        -- Obtener nivel antes
        SELECT nivel_id INTO v_nivel_antes FROM usuario WHERE id = v_usuario_id;

        -- Insertar movimiento manual
        INSERT INTO movimiento_xp (usuario_id, tipo_actividad_id, xp_ganada)
        VALUES (v_usuario_id, 1, 500); -- 500 XP

        -- Recalcular XP
        PERFORM actualizar_xp_usuario(v_usuario_id);

        -- Obtener nivel después
        SELECT nivel_id INTO v_nivel_despues FROM usuario WHERE id = v_usuario_id;

        -- Limpiar
        DELETE FROM movimiento_xp WHERE usuario_id = v_usuario_id AND xp_ganada = 500;
        PERFORM actualizar_xp_usuario(v_usuario_id);

        IF v_nivel_despues != v_nivel_antes THEN
            RAISE NOTICE '✓ Función actualizar_xp_usuario funciona (nivel se actualizó)';
        ELSE
            RAISE NOTICE '✗ Función actualizar_xp_usuario NO funciona (nivel NO se actualizó)';
        END IF;
    END;
END
$$;

-- 2.5 Verificar función solicitar_vinculacion
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 2.5: Función solicitar_vinculacion ===';

    DECLARE
        v_semillero_id INTEGER := 1;
        v_usuario_id INTEGER := 11; -- Ana Martínez (pendiente)
        v_vinculacion_id INTEGER;
    BEGIN
        -- Solicitar vinculación
        SELECT solicitar_vinculacion(v_semillero_id, v_usuario_id) INTO v_vinculacion_id;

        -- Verificar que se creó
        IF EXISTS (SELECT 1 FROM semillero_integrante WHERE id = v_vinculacion_id AND estado = 'solicitada') THEN
            RAISE NOTICE '✓ Función solicitar_vinculacion funciona (vinculación creada)';
        ELSE
            RAISE NOTICE '✗ Función solicitar_vinculacion NO funciona (vinculación NO creada)';
        END IF;

        -- Verificar que se creó notificación al líder
        IF EXISTS (
            SELECT 1 FROM notificacion n
            JOIN semillero s ON n.usuario_id = s.lider_id
            WHERE n.referencia_tipo = 'semillero_integrante'
            AND n.referencia_id = v_vinculacion_id
            AND n.tipo = 'vinculacion_solicitada'
        ) THEN
            RAISE NOTICE '✓ Función solicitar_vinculacion funciona (notificación creada)';
        ELSE
            RAISE NOTICE '✗ Función solicitar_vinculacion NO funciona (notificación NO creada)';
        END IF;

        -- Limpiar
        DELETE FROM semillero_integrante WHERE id = v_vinculacion_id;
        DELETE FROM notificacion WHERE referencia_tipo = 'semillero_integrante' AND referencia_id = v_vinculacion_id;
    END;
END
$$;

-- 2.6 Verificar función resolver_vinculacion (aprobación)
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 2.6: Función resolver_vinculacion (aprobación) ===';

    DECLARE
        v_semillero_id INTEGER := 1;
        v_usuario_id INTEGER := 11;
        v_revisor_id INTEGER := 2; -- Docente líder
        v_vinculacion_id INTEGER;
        v_xp_antes INTEGER;
        v_xp_despues INTEGER;
    BEGIN
        -- Obtener XP antes
        SELECT xp_total INTO v_xp_antes FROM usuario WHERE id = v_usuario_id;

        -- Solicitar vinculación
        SELECT solicitar_vinculacion(v_semillero_id, v_usuario_id) INTO v_vinculacion_id;

        -- Aprobar vinculación
        PERFORM resolver_vinculacion(v_vinculacion_id, 'aprobada', v_revisor_id);

        -- Obtener XP después
        SELECT xp_total INTO v_xp_despues FROM usuario WHERE id = v_usuario_id;

        -- Limpiar
        DELETE FROM movimiento_xp WHERE referencia_tipo = 'semillero_integrante' AND referencia_id = v_vinculacion_id;
        DELETE FROM semillero_integrante WHERE id = v_vinculacion_id;
        DELETE FROM notificacion WHERE referencia_tipo = 'semillero_integrante' AND referencia_id = v_vinculacion_id;
        UPDATE usuario SET xp_total = v_xp_antes WHERE id = v_usuario_id;

        IF v_xp_despues = v_xp_antes + 100 THEN -- XP base de vinculación
            RAISE NOTICE '✓ Función resolver_vinculacion funciona (XP otorgada)';
        ELSE
            RAISE NOTICE '✗ Función resolver_vinculacion NO funciona (XP NO otorgada)';
        END IF;
    END;
END
$$;

-- ==========================================
-- PRUEBA 3: VISTAS DE ANALÍTICA
-- ==========================================

-- 3.1 Verificar vista v_ranking_semilleros
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.1: Vista v_ranking_semilleros ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_ranking_semilleros;

        IF v_count > 0 THEN
            RAISE NOTICE '✓ Vista v_ranking_semilleros funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_ranking_semilleros NO funciona (retornó 0 registros)';
        END IF;
    END;
END
$$;

-- 3.2 Verificar vista v_ranking_investigadores
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.2: Vista v_ranking_investigadores ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_ranking_investigadores;

        IF v_count > 0 THEN
            RAISE NOTICE '✓ Vista v_ranking_investigadores funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_ranking_investigadores NO funciona (retornó 0 registros)';
        END IF;
    END;
END
$$;

-- 3.3 Verificar vista v_xp_por_usuario
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.3: Vista v_xp_por_usuario ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_xp_por_usuario;

        IF v_count > 0 THEN
            RAISE NOTICE '✓ Vista v_xp_por_usuario funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_xp_por_usuario NO funciona (retornó 0 registros)';
        END IF;
    END;
END
$$;

-- 3.4 Verificar vista v_impacto_publicaciones
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.4: Vista v_impacto_publicaciones ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_impacto_publicaciones;

        IF v_count > 0 THEN
            RAISE NOTICE '✓ Vista v_impacto_publicaciones funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_impacto_publicaciones NO funciona (retornó 0 registros)';
        END IF;
    END;
END
$$;

-- 3.5 Verificar vista v_indicadores_facultad
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.5: Vista v_indicadores_facultad ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_indicadores_facultad;

        IF v_count > 0 THEN
            RAISE NOTICE '✓ Vista v_indicadores_facultad funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_indicadores_facultad NO funciona (retornó 0 registros)';
        END IF;
    END;
END
$$;

-- 3.6 Verificar vista v_hoja_vida_investigativa
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.6: Vista v_hoja_vida_investigativa ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_hoja_vida_investigativa;

        IF v_count > 0 THEN
            RAISE NOTICE '✓ Vista v_hoja_vida_investigativa funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_hoja_vida_investigativa NO funciona (retornó 0 registros)';
        END IF;
    END;
END
$$;

-- 3.7 Verificar vista v_kpis_institucionales
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.7: Vista v_kpis_institucionales ===';

    DECLARE
        v_semilleros INTEGER;
        v_usuarios INTEGER;
        v_publicaciones INTEGER;
    BEGIN
        SELECT semilleros_activos, usuarios_activos, publicaciones_totales
        INTO v_semilleros, v_usuarios, v_publicaciones
        FROM v_kpis_institucionales;

        IF v_semilleros > 0 AND v_usuarios > 0 AND v_publicaciones > 0 THEN
            RAISE NOTICE '✓ Vista v_kpis_institucionales funciona (semilleros: %, usuarios: %, publicaciones: %)', v_semilleros, v_usuarios, v_publicaciones;
        ELSE
            RAISE NOTICE '✗ Vista v_kpis_institucionales NO funciona (valores incorrectos)';
        END IF;
    END;
END
$$;

-- 3.8 Verificar vista v_logros_pendientes
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.8: Vista v_logros_pendientes ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_logros_pendientes;

        IF v_count >= 0 THEN -- Puede ser 0 si no hay pendientes
            RAISE NOTICE '✓ Vista v_logros_pendientes funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_logros_pendientes NO funciona';
        END IF;
    END;
END
$$;

-- 3.9 Verificar vista v_cuentas_pendientes
DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 3.9: Vista v_cuentas_pendientes ===';

    DECLARE
        v_count INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM v_cuentas_pendientes;

        IF v_count >= 0 THEN -- Puede ser 0 si no hay pendientes
            RAISE NOTICE '✓ Vista v_cuentas_pendientes funciona (retornó % registros)', v_count;
        ELSE
            RAISE NOTICE '✗ Vista v_cuentas_pendientes NO funciona';
        END IF;
    END;
END
$$;

-- ==========================================
-- PRUEBA 4: FLUJO COMPLETO DE LOGRO
-- ==========================================

DO $$
BEGIN
    RAISE NOTICE '=== PRUEBA 4: Flujo completo de logro ===';

    DECLARE
        v_usuario_id INTEGER := 6; -- Camilo
        v_logro_id INTEGER;
        v_xp_antes INTEGER;
        v_xp_despues INTEGER;
        v_nivel_antes INTEGER;
        v_nivel_despues INTEGER;
    BEGIN
        -- Obtener XP y nivel antes
        SELECT xp_total, nivel_id INTO v_xp_antes, v_nivel_antes FROM usuario WHERE id = v_usuario_id;

        -- Insertar logro
        INSERT INTO logro (usuario_id, tipo, titulo, descripcion, estado)
        VALUES (v_usuario_id, 'articulo', 'Artículo de prueba', 'Artículo de prueba para verificación', 'enviado')
        RETURNING id INTO v_logro_id;

        -- Aprobar logro (esto debería insertar XP, actualizar nivel, otorgar insignias)
        UPDATE logro
        SET estado = 'aprobado', validado_por = 1, fecha_validacion = CURRENT_TIMESTAMP
        WHERE id = v_logro_id;

        -- Obtener XP y nivel después
        SELECT xp_total, nivel_id INTO v_xp_despues, v_nivel_despues FROM usuario WHERE id = v_usuario_id;

        -- Verificar que XP aumentó
        IF v_xp_despues > v_xp_antes THEN
            RAISE NOTICE '✓ Flujo de logro: XP aumentó de % a %', v_xp_antes, v_xp_despues;
        ELSE
            RAISE NOTICE '✗ Flujo de logro: XP NO aumentó';
        END IF;

        -- Verificar que se creó movimiento XP
        IF EXISTS (
            SELECT 1 FROM movimiento_xp
            WHERE usuario_id = v_usuario_id
            AND referencia_tipo = 'logro'
            AND referencia_id = v_logro_id
        ) THEN
            RAISE NOTICE '✓ Flujo de logro: Movimiento XP creado';
        ELSE
            RAISE NOTICE '✗ Flujo de logro: Movimiento XP NO creado';
        END IF;

        -- Verificar que se creó notificación
        IF EXISTS (
            SELECT 1 FROM notificacion
            WHERE usuario_id = v_usuario_id
            AND referencia_tipo = 'logro'
            AND referencia_id = v_logro_id
            AND tipo = 'logro_aprobado'
        ) THEN
            RAISE NOTICE '✓ Flujo de logro: Notificación creada';
        ELSE
            RAISE NOTICE '✗ Flujo de logro: Notificación NO creada';
        END IF;

        -- Limpiar
        DELETE FROM movimiento_xp WHERE referencia_tipo = 'logro' AND referencia_id = v_logro_id;
        DELETE FROM notificacion WHERE referencia_tipo = 'logro' AND referencia_id = v_logro_id;
        DELETE FROM logro WHERE id = v_logro_id;
        UPDATE usuario SET xp_total = v_xp_antes, nivel_id = v_nivel_antes WHERE id = v_usuario_id;
    END;
END
$$;

-- ==========================================
-- RESUMEN FINAL
-- ==========================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'PRUEBAS COMPLETADAS';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Si todas las pruebas muestran ✓, la BD está correctamente configurada.';
    RAISE NOTICE 'Si hay ✗, revise los errores en los logs.';
END
$$;
