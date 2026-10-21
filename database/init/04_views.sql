-- ==========================================
-- 04_views.sql
-- Vistas de analítica y ranking
-- ==========================================

-- ==========================================
-- VISTA: RANKING DE SEMILLEROS
-- ==========================================

CREATE OR REPLACE VIEW v_ranking_semilleros AS
SELECT
    s.id AS semillero_id,
    s.nombre AS semillero_nombre,
    f.nombre AS facultad,
    p.nombre AS programa,
    COALESCE(SUM(u.xp_total), 0) AS xp_total,
    n.numero AS nivel,
    n.estrellas,
    COUNT(DISTINCT si.usuario_id) AS num_integrantes,
    COUNT(DISTINCT pr.id) AS num_proyectos,
    COUNT(DISTINCT pub.id) AS num_publicaciones
FROM semillero s
LEFT JOIN facultad f ON s.facultad_id = f.id
LEFT JOIN programa p ON s.programa_id = p.id
LEFT JOIN semillero_integrante si ON s.id = si.semillero_id AND si.estado = 'aprobada'
LEFT JOIN usuario u ON si.usuario_id = u.id
LEFT JOIN nivel n ON u.nivel_id = n.id
LEFT JOIN proyecto pr ON s.id = pr.semillero_id AND pr.eliminado_en IS NULL
LEFT JOIN publicacion pub ON s.id = pub.semillero_id AND pub.eliminado_en IS NULL
WHERE s.eliminado_en IS NULL AND s.activo = TRUE
GROUP BY s.id, s.nombre, f.nombre, p.nombre, n.numero, n.estrellas
ORDER BY xp_total DESC;

COMMENT ON VIEW v_ranking_semilleros IS 'Ranking de semilleros ordenado por XP total de sus integrantes';

-- ==========================================
-- VISTA: RANKING DE INVESTIGADORES
-- ==========================================

CREATE OR REPLACE VIEW v_ranking_investigadores AS
SELECT
    u.id AS usuario_id,
    u.nombres,
    u.apellidos,
    u.email,
    r.nombre AS rol,
    u.xp_total,
    n.numero AS nivel,
    n.estrellas,
    COUNT(DISTINCT ui.insignia_id) AS num_insignias,
    COUNT(DISTINCT si.semillero_id) AS num_semilleros,
    COUNT(DISTINCT pub.id) AS num_publicaciones,
    COUNT(DISTINCT l.id) AS num_logros_aprobados
FROM usuario u
JOIN rol r ON u.rol_id = r.id
LEFT JOIN nivel n ON u.nivel_id = n.id
LEFT JOIN usuario_insignia ui ON u.id = ui.usuario_id
LEFT JOIN semillero_integrante si ON u.id = si.usuario_id AND si.estado = 'aprobada'
LEFT JOIN publicacion pub ON u.id = pub.usuario_id AND pub.eliminado_en IS NULL
LEFT JOIN logro l ON u.id = l.usuario_id AND l.estado = 'aprobado'
WHERE u.eliminado_en IS NULL AND u.estado = 'aprobada'
GROUP BY u.id, u.nombres, u.apellidos, u.email, r.nombre, u.xp_total, n.numero, n.estrellas
ORDER BY u.xp_total DESC;

COMMENT ON VIEW v_ranking_investigadores IS 'Ranking de investigadores ordenado por XP total';

-- ==========================================
-- VISTA: XP POR USUARIO
-- ==========================================

CREATE OR REPLACE VIEW v_xp_por_usuario AS
SELECT
    u.id AS usuario_id,
    u.nombres,
    u.apellidos,
    u.xp_total,
    n.numero AS nivel,
    n.estrellas,
    COALESCE(SUM(mx.xp_ganada), 0) AS xp_ganada_total,
    COUNT(mx.id) AS num_movimientos,
    MAX(mx.creado_en) AS ultimo_movimiento
FROM usuario u
LEFT JOIN nivel n ON u.nivel_id = n.id
LEFT JOIN movimiento_xp mx ON u.id = mx.usuario_id
WHERE u.eliminado_en IS NULL
GROUP BY u.id, u.nombres, u.apellidos, u.xp_total, n.numero, n.estrellas
ORDER BY u.xp_total DESC;

COMMENT ON VIEW v_xp_por_usuario IS 'Detalle de XP por usuario con historial de movimientos';

-- ==========================================
-- VISTA: IMPACTO DE PUBLICACIONES
-- ==========================================

CREATE OR REPLACE VIEW v_impacto_publicaciones AS
SELECT
    pub.id AS publicacion_id,
    pub.titulo,
    pub.contenido,
    cp.nombre AS categoria,
    u.nombres AS autor,
    u.apellidos,
    pub.creado_en,
    COUNT(DISTINCT c.id) AS num_comentarios,
    COUNT(DISTINCT r.id) AS num_reacciones,
    COUNT(DISTINCT comp.id) AS num_compartidos,
    -- Puntuación de impacto (ponderado)
    (COUNT(DISTINCT c.id) * 1 + COUNT(DISTINCT r.id) * 2 + COUNT(DISTINCT comp.id) * 3) AS puntaje_impacto
FROM publicacion pub
JOIN categoria_publicacion cp ON pub.categoria_id = cp.id
JOIN usuario u ON pub.usuario_id = u.id
LEFT JOIN comentario c ON pub.id = c.publicacion_id AND c.eliminado_en IS NULL
LEFT JOIN reaccion r ON pub.id = r.publicacion_id
LEFT JOIN compartido comp ON pub.id = comp.publicacion_id
WHERE pub.eliminado_en IS NULL
GROUP BY pub.id, pub.titulo, pub.contenido, cp.nombre, u.nombres, u.apellidos, pub.creado_en
ORDER BY puntaje_impacto DESC;

COMMENT ON VIEW v_impacto_publicaciones IS 'Impacto de publicaciones basado en comentarios, reacciones y compartidos';

-- ==========================================
-- VISTA: INDICADORES INSTITUCIONALES POR FACULTAD
-- ==========================================

CREATE OR REPLACE VIEW v_indicadores_facultad AS
SELECT
    f.id AS facultad_id,
    f.nombre AS facultad,
    COUNT(DISTINCT s.id) AS num_semilleros,
    COUNT(DISTINCT u.id) AS num_usuarios,
    COALESCE(SUM(u.xp_total), 0) AS xp_total_facultad,
    COUNT(DISTINCT pr.id) AS num_proyectos,
    COUNT(DISTINCT prod.id) AS num_productos,
    COUNT(DISTINCT pub.id) AS num_publicaciones,
    COUNT(DISTINCT l.id) AS num_logros_aprobados
FROM facultad f
LEFT JOIN semillero s ON f.id = s.facultad_id AND s.eliminado_en IS NULL AND s.activo = TRUE
LEFT JOIN semillero_integrante si ON s.id = si.semillero_id AND si.estado = 'aprobada'
LEFT JOIN usuario u ON si.usuario_id = u.id AND u.eliminado_en IS NULL
LEFT JOIN proyecto pr ON s.id = pr.semillero_id AND pr.eliminado_en IS NULL
LEFT JOIN producto prod ON pr.id = prod.proyecto_id
LEFT JOIN publicacion pub ON s.id = pub.semillero_id AND pub.eliminado_en IS NULL
LEFT JOIN logro l ON u.id = l.usuario_id AND l.estado = 'aprobado'
GROUP BY f.id, f.nombre
ORDER BY xp_total_facultad DESC;

COMMENT ON VIEW v_indicadores_facultad IS 'Indicadores institucionales agrupados por facultad';

-- ==========================================
-- VISTA: INDICADORES INSTITUCIONALES POR PROGRAMA
-- ==========================================

CREATE OR REPLACE VIEW v_indicadores_programa AS
SELECT
    p.id AS programa_id,
    p.nombre AS programa,
    f.nombre AS facultad,
    COUNT(DISTINCT up.usuario_id) AS num_usuarios,
    COALESCE(SUM(u.xp_total), 0) AS xp_total_programa,
    COUNT(DISTINCT si.semillero_id) AS num_semilleros,
    COUNT(DISTINCT pub.id) AS num_publicaciones,
    COUNT(DISTINCT l.id) AS num_logros_aprobados
FROM programa p
JOIN facultad f ON p.facultad_id = f.id
LEFT JOIN usuario_programa up ON p.id = up.programa_id AND up.actual = TRUE
LEFT JOIN usuario u ON up.usuario_id = u.id AND u.eliminado_en IS NULL
LEFT JOIN semillero_integrante si ON u.id = si.usuario_id AND si.estado = 'aprobada'
LEFT JOIN publicacion pub ON u.id = pub.usuario_id AND pub.eliminado_en IS NULL
LEFT JOIN logro l ON u.id = l.usuario_id AND l.estado = 'aprobado'
GROUP BY p.id, p.nombre, f.nombre
ORDER BY xp_total_programa DESC;

COMMENT ON VIEW v_indicadores_programa IS 'Indicadores institucionales agrupados por programa académico';

-- ==========================================
-- VISTA: HOJA DE VIDA INVESTIGATIVA
-- ==========================================

CREATE OR REPLACE VIEW v_hoja_vida_investigativa AS
SELECT
    u.id AS usuario_id,
    u.nombres,
    u.apellidos,
    u.email,
    pi.biografia,
    pi.intereses,
    pi.orcid,
    pi.cvlac,
    r.nombre AS rol,
    f.nombre AS facultad,
    prog.nombre AS programa,
    u.xp_total,
    n.numero AS nivel,
    n.estrellas,
    -- Logros por tipo
    COUNT(DISTINCT CASE WHEN l.tipo = 'articulo' THEN l.id END) AS num_articulos,
    COUNT(DISTINCT CASE WHEN l.tipo = 'ponencia' THEN l.id END) AS num_ponencias,
    COUNT(DISTINCT CASE WHEN l.tipo = 'proyecto' THEN l.id END) AS num_proyectos_logros,
    COUNT(DISTINCT CASE WHEN l.tipo = 'patente' THEN l.id END) AS num_patentes,
    -- Actividades
    COUNT(DISTINCT si.semillero_id) AS num_semilleros,
    COUNT(DISTINCT pr.id) AS num_proyectos_participa,
    COUNT(DISTINCT pub.id) AS num_publicaciones,
    COUNT(DISTINCT pe.id) AS num_eventos_participados,
    -- Insignias
    ARRAY_AGG(DISTINCT i.nombre) AS insignias
FROM usuario u
LEFT JOIN perfil_investigador pi ON u.id = pi.usuario_id
LEFT JOIN rol r ON u.rol_id = r.id
LEFT JOIN usuario_programa up ON u.id = up.usuario_id AND up.actual = TRUE
LEFT JOIN programa prog ON up.programa_id = prog.id
LEFT JOIN facultad f ON prog.facultad_id = f.id
LEFT JOIN nivel n ON u.nivel_id = n.id
LEFT JOIN logro l ON u.id = l.usuario_id AND l.estado = 'aprobado'
LEFT JOIN semillero_integrante si ON u.id = si.usuario_id AND si.estado = 'aprobada'
LEFT JOIN proyecto_integrante pri ON u.id = pri.usuario_id
LEFT JOIN proyecto pr ON pri.proyecto_id = pr.id
LEFT JOIN publicacion pub ON u.id = pub.usuario_id AND pub.eliminado_en IS NULL
LEFT JOIN participacion_evento pe ON u.id = pe.usuario_id
LEFT JOIN usuario_insignia ui ON u.id = ui.usuario_id
LEFT JOIN insignia i ON ui.insignia_id = i.id
WHERE u.eliminado_en IS NULL
GROUP BY u.id, u.nombres, u.apellidos, u.email, pi.biografia, pi.intereses, pi.orcid, pi.cvlac,
         r.nombre, f.nombre, prog.nombre, u.xp_total, n.numero, n.estrellas
ORDER BY u.xp_total DESC;

COMMENT ON VIEW v_hoja_vida_investigativa IS 'Hoja de vida investigativa completa de cada usuario';

-- ==========================================
-- VISTA: KPIs INSTITUCIONALES
-- ==========================================

CREATE OR REPLACE VIEW v_kpis_institucionales AS
SELECT
    COUNT(DISTINCT s.id) AS semilleros_activos,
    COUNT(DISTINCT u.id) AS usuarios_activos,
    COALESCE(SUM(u.xp_total), 0) AS xp_total_institucion,
    COUNT(DISTINCT pub.id) AS publicaciones_totales,
    COUNT(DISTINCT pr.id) AS proyectos_en_curso,
    COUNT(DISTINCT l.id) AS logros_validados,
    COUNT(DISTINCT e.id) AS eventos_totales,
    COUNT(DISTINCT c.id) AS convocatorias_abiertas
FROM usuario u
LEFT JOIN semillero_integrante si ON u.id = si.usuario_id AND si.estado = 'aprobada'
LEFT JOIN semillero s ON si.semillero_id = s.id AND s.eliminado_en IS NULL AND s.activo = TRUE
LEFT JOIN publicacion pub ON u.id = pub.usuario_id AND pub.eliminado_en IS NULL
LEFT JOIN proyecto pr ON s.id = pr.semillero_id AND pr.eliminado_en IS NULL AND pr.estado = 'en_curso'
LEFT JOIN logro l ON u.id = l.usuario_id AND l.estado = 'aprobado'
LEFT JOIN participacion_evento pe ON u.id = pe.usuario_id
LEFT JOIN evento e ON pe.evento_id = e.id
LEFT JOIN convocatoria c ON c.estado = 'publicada'
WHERE u.eliminado_en IS NULL AND u.estado = 'aprobada';

COMMENT ON VIEW v_kpis_institucionales IS 'KPIs generales de la institución (dashboard)';

-- ==========================================
-- VISTA: LOGROS PENDIENTES DE VALIDACIÓN
-- ==========================================

CREATE OR REPLACE VIEW v_logros_pendientes AS
SELECT
    l.id AS logro_id,
    u.nombres,
    u.apellidos,
    u.email,
    l.tipo,
    l.titulo,
    l.descripcion,
    l.creado_en AS fecha_envio,
    -- Evidencias asociadas
    ARRAY_AGG(e.nombre_archivo) AS evidencias
FROM logro l
JOIN usuario u ON l.usuario_id = u.id
LEFT JOIN logro_evidencia le ON l.id = le.logro_id
LEFT JOIN evidencia e ON le.evidencia_id = e.id
WHERE l.estado = 'enviado'
GROUP BY l.id, u.nombres, u.apellidos, u.email, l.tipo, l.titulo, l.descripcion, l.creado_en
ORDER BY l.creado_en DESC;

COMMENT ON VIEW v_logros_pendientes IS 'Logros pendientes de validación por administrador';

-- ==========================================
-- VISTA: CUENTAS PENDIENTES DE VALIDACIÓN
-- ==========================================

CREATE OR REPLACE VIEW v_cuentas_pendientes AS
SELECT
    u.id AS usuario_id,
    u.nombres,
    u.apellidos,
    u.email,
    r.nombre AS rol_solicitado,
    prog.nombre AS programa,
    u.documento_ruta,
    u.creado_en AS fecha_registro
FROM usuario u
JOIN rol r ON u.rol_id = r.id
LEFT JOIN usuario_programa up ON u.id = up.usuario_id AND up.actual = TRUE
LEFT JOIN programa prog ON up.programa_id = prog.id
WHERE u.estado = 'pendiente' AND u.eliminado_en IS NULL
ORDER BY u.creado_en DESC;

COMMENT ON VIEW v_cuentas_pendientes IS 'Cuentas pendientes de validación por administrador';

-- ==========================================
-- VISTA: HISTORIAL DE XP DE UN USUARIO
-- ==========================================

CREATE OR REPLACE VIEW v_historial_xp_usuario AS
SELECT
    mx.id,
    mx.usuario_id,
    u.nombres,
    u.apellidos,
    tax.tipo AS actividad,
    tax.xp_base,
    mx.xp_ganada,
    mx.referencia_tipo,
    mx.referencia_id,
    mx.creado_en
FROM movimiento_xp mx
JOIN usuario u ON mx.usuario_id = u.id
JOIN tipo_actividad_xp tax ON mx.tipo_actividad_id = tax.id
ORDER BY mx.creado_en DESC;

COMMENT ON VIEW v_historial_xp_usuario IS 'Historial completo de movimientos de XP';
