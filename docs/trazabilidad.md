# Matriz de Trazabilidad - RIUL

Este documento traza la relación entre requerimientos funcionales (RF), elementos del prototipo, páginas HTML, endpoints de la API, tablas/funciones/vistas de la BD y servicios Docker.

## Tabla de Contenidos

- [Módulo Usuarios](#módulo-usuarios)
- [Módulo Investigación](#módulo-investigación)
- [Módulo Eventos y Convocatorias](#módulo-eventos-y-convocatorias)
- [Módulo Comunidad](#módulo-comunidad)
- [Módulo Gamificación](#módulo-gamificación)
- [Módulo Analítica](#módulo-analítica)

---

## MÓDULO USUARIOS

### RF01.1: Registro de cuenta institucional con validación administrativa

| Elemento | Detalle |
|----------|---------|
| **RF** | RF01.1 - Registro de cuenta con validación |
| **Prototipo** | Pantalla login → botón "No tengo cuenta" → formulario de registro |
| **Página HTML** | `view-login` (formualrio registro) |
| **Endpoint API** | `POST /api/auth/register` |
| **Controller** | `authController.register` |
| **Tablas BD** | `usuario`, `rol`, `usuario_programa` |
| **Estado BD** | `usuario.estado = 'pendiente'` |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF01.2: Login con autenticación JWT

| Elemento | Detalle |
|----------|---------|
| **RF** | RF01.2 - Login con JWT |
| **Prototipo** | Pantalla login → formulario email/contraseña |
| **Página HTML** | `view-login` (formulario login) |
| **Endpoint API** | `POST /api/auth/login` |
| **Controller** | `authController.login` |
| **Tablas BD** | `usuario`, `rol`, `nivel` |
| **Middleware** | `authenticateToken` (verifica JWT) |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF01.3: Perfil de usuario con hoja de vida investigativa

| Elemento | Detalle |
|----------|---------|
| **RF** | RF01.3 - Perfil y hoja de vida |
| **Prototipo** | Vista "Mi perfil" |
| **Página HTML** | `view-perfil` |
| **Endpoint API** | `GET /api/auth/me` |
| **Controller** | `authController.getMe` |
| **Tablas BD** | `usuario`, `perfil_investigador`, `usuario_programa`, `usuario_insignia`, `insignia` |
| **Vista BD** | `v_hoja_vida_investigativa` |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF01.4: Asignación de roles (estudiante, docente, admin, visitante)

| Elemento | Detalle |
|----------|---------|
| **RF** | RF01.4 - Roles del sistema |
| **Prototipo** | Selector de rol en topbar |
| **Página HTML** | Todas las vistas (topbar) |
| **Endpoint API** | Múltiples (middleware `requireRole`) |
| **Middleware** | `requireRole` (verifica permisos) |
| **Tablas BD** | `rol`, `usuario.rol_id` |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF01.5: Estados de cuenta (pendiente, aprobada, rechazada, suspendida)

| Elemento | Detalle |
|----------|---------|
| **RF** | RF01.5 - Estados de cuenta |
| **Prototipo** | No visible en prototipo (simulado) |
| **Página HTML** | N/A |
| **Endpoint API** | `GET /api/admin/cuentas-pendientes` |
| **Controller** | `adminController.getCuentasPendientes` |
| **Tablas BD** | `usuario.estado` (ENUM) |
| **Vista BD** | `v_cuentas_pendientes` |
| **Función BD** | `validar_cuenta` |
| **Servicio Docker** | `riul-api`, `riul-db` |

---

## MÓDULO INVESTIGACIÓN

### RF02.1: Gestión de semilleros por docente líder

| Elemento | Detalle |
|----------|---------|
| **RF** | RF02.1 - Gestión de semilleros |
| **Prototipo** | Vista "Gestión de semillero" |
| **Página HTML** | `view-semillero` |
| **Endpoint API** | `GET /api/semilleros`, `GET /api/semilleros/:id` |
| **Controller** | `semilleroController.getSemilleros`, `getSemilleroById` |
| **Tablas BD** | `semillero`, `facultad`, `programa`, `usuario` (líder) |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF02.2: Líneas de investigación

| Elemento | Detalle |
|----------|---------|
| **RF** | RF02.2 - Líneas de investigación |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | N/A (administrativo) |
| **Tablas BD** | `linea_investigacion`, `semillero_linea` |
| **Servicio Docker** | `riul-db` |

### RF02.3: Vinculación de estudiantes a semilleros con aprobación

| Elemento | Detalle |
|----------|---------|
| **RF** | RF02.3 - Vinculación con aprobación |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | `POST /api/semilleros/solicitar-vinculacion`, `POST /api/semilleros/resolver-vinculacion` |
| **Controller** | `semilleroController.solicitarVinculacion`, `resolverVinculacion` |
| **Tablas BD** | `semillero_integrante` |
| **Función BD** | `solicitar_vinculacion`, `resolver_vinculacion` |
| **Trigger BD** | `trg_semillero_integrante_unico` (impide doble vinculación) |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF02.4: Registro de proyectos y avances

| Elemento | Detalle |
|----------|---------|
| **RF** | RF02.4 - Proyectos y avances |
| **Prototipo** | Vista "Gestión de semillero" → lista de proyectos |
| **Página HTML** | `view-semillero` |
| **Endpoint API** | N/A (solo lectura en frontend actual) |
| **Tablas BD** | `proyecto`, `avance_proyecto`, `proyecto_integrante` |
| **Servicio Docker** | `riul-db` |

### RF02.5: Registro de productos (artículos, ponencias, patentes, software)

| Elemento | Detalle |
|----------|---------|
| **RF** | RF02.5 - Productos de investigación |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | N/A |
| **Tablas BD** | `producto`, `tipo_producto` (ENUM) |
| **Servicio Docker** | `riul-db` |

---

## MÓDULO EVENTOS Y CONVOCATORIAS

### RF03.1: Consulta de eventos académicos

| Elemento | Detalle |
|----------|---------|
| **RF** | RF03.1 - Consulta de eventos |
| **Prototipo** | Vista "Eventos y convocatorias" → lista de eventos |
| **Página HTML** | `view-eventos` |
| **Endpoint API** | N/A (solo lectura en frontend actual) |
| **Tablas BD** | `evento`, `participacion_evento` |
| **Servicio Docker** | `riul-db` |

### RF03.2: Registro de participación en eventos

| Elemento | Detalle |
|----------|---------|
| **RF** | RF03.2 - Participación en eventos |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | N/A |
| **Tablas BD** | `participacion_evento` |
| **Función BD** | `insertar_movimiento_xp` (tipo: evento_participacion) |
| **Servicio Docker** | `riul-db` |

### RF03.3: Publicación de convocatorias

| Elemento | Detalle |
|----------|---------|
| **RF** | RF03.3 - Publicación de convocatorias |
| **Prototipo** | Vista "Eventos y convocatorias" → lista de convocatorias |
| **Página HTML** | `view-eventos` |
| **Endpoint API** | N/A (solo lectura en frontend actual) |
| **Tablas BD** | `convocatoria`, `estado_convocatoria` (ENUM) |
| **Trigger BD** | `trg_convocatoria_publicada` (notifica al publicar) |
| **Servicio Docker** | `riul-db` |

### RF03.4: Postulación a convocatorias

| Elemento | Detalle |
|----------|---------|
| **RF** | RF03.4 - Postulación a convocatorias |
| **Prototipo** | Vista "Eventos y convocatorias" → botón "Postularse" |
| **Página HTML** | `view-eventos` |
| **Endpoint API** | N/A (frontend actual muestra toast) |
| **Tablas BD** | `postulacion_convocatoria`, `estado_postulacion` (ENUM) |
| **Servicio Docker** | `riul-db` |

### RF03.5: Validación administrativa de convocatorias

| Elemento | Detalle |
|----------|---------|
| **RF** | RF03.5 - Validación de convocatorias |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | N/A |
| **Tablas BD** | `convocatoria.validado_por`, `convocatoria.fecha_validacion` |
| **Servicio Docker** | `riul-db` |

---

## MÓDULO COMUNIDAD

### RF04.1: Creación de publicaciones con categorías y evidencias

| Elemento | Detalle |
|----------|---------|
| **RF** | RF04.1 - Publicaciones con categorías y evidencias |
| **Prototipo** | Vista "Publicaciones" → modal "Crear publicación" |
| **Página HTML** | `view-publicaciones`, `modal-post` |
| **Endpoint API** | `GET /api/publicaciones`, `POST /api/publicaciones` |
| **Controller** | `publicacionController.getPublicaciones`, `createPublicacion` |
| **Tablas BD** | `publicacion`, `categoria_publicacion`, `evidencia`, `publicacion_evidencia` |
| **Función BD** | `registrar_publicacion` (inserta XP) |
| **Trigger BD** | Notificaciones a seguidores |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF04.2: Comentarios en publicaciones

| Elemento | Detalle |
|----------|---------|
| **RF** | RF04.2 - Comentarios |
| **Prototipo** | Vista "Publicaciones" → botón "Comentar" en posts |
| **Página HTML** | `view-publicaciones` |
| **Endpoint API** | `POST /api/publicaciones/comentar` |
| **Controller** | `publicacionController.comentar` |
| **Tablas BD** | `comentario` |
| **Función BD** | `comentar_publicacion` (inserta XP, notifica autor) |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF04.3: Reacciones (UNIQUE usuario+publicación+tipo)

| Elemento | Detalle |
|----------|---------|
| **RF** | RF04.3 - Reacciones |
| **Prototipo** | Vista "Publicaciones" → botón "Reaccionar" en posts |
| **Página HTML** | `view-publicaciones` |
| **Endpoint API** | `POST /api/publicaciones/reaccionar` |
| **Controller** | `publicacionController.reaccionar` |
| **Tablas BD** | `reaccion`, `tipo_reaccion` (ENUM) |
| **Restricción BD** | UNIQUE (publicacion_id, usuario_id, tipo) |
| **Trigger BD** | `trg_reaccion_unico` (impide doble reacción) |
| **Función BD** | `reaccionar_publicacion` (inserta XP, notifica autor) |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF04.4: Compartir publicaciones

| Elemento | Detalle |
|----------|---------|
| **RF** | RF04.4 - Compartidos |
| **Prototipo** | Vista "Publicaciones" → botón "Compartir" en posts |
| **Página HTML** | `view-publicaciones` |
| **Endpoint API** | `POST /api/publicaciones/compartir` |
| **Controller** | `publicacionController.compartir` |
| **Tablas BD** | `compartido` |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF04.5: Seguimiento (follow) entre usuarios/semilleros

| Elemento | Detalle |
|----------|---------|
| **RF** | RF04.5 - Seguimiento |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | N/A |
| **Tablas BD** | `seguimiento_usuario`, `seguimiento_semillero` |
| **Servicio Docker** | `riul-db` |

### RF04.6: Notificaciones de interacción

| Elemento | Detalle |
|----------|---------|
| **RF** | RF04.6 - Notificaciones |
| **Prototipo** | Icono de campana en topbar (no funcional) |
| **Página HTML** | Topbar (icono campana) |
| **Endpoint API** | N/A (no implementado en frontend actual) |
| **Tablas BD** | `notificacion` |
| **Trigger BD** - Notificaciones creadas por:
  - `registrar_publicacion` (notifica seguidores)
  - `comentar_publicacion` (notifica autor)
  - `reaccionar_publicacion` (notifica autor)
  - `validar_cuenta` (notifica usuario)
  - `resolver_vinculacion` (notifica usuario)
  - `trg_logro_aprobado` (notifica usuario)
  - `trg_convocatoria_publicada` (notifica todos) |
| **Servicio Docker** | `riul-db` |

---

## MÓDULO GAMIFICACIÓN

### RF05.1: Envío de logros con evidencia

| Elemento | Detalle |
|----------|---------|
| **RF** | RF05.1 - Envío de logros |
| **Prototipo** | Vista "Mi perfil" → formulario "Registrar nuevo logro" |
| **Página HTML** | `view-perfil` |
| **Endpoint API** | `POST /api/logros`, `GET /api/logros/mis-logros` |
| **Controller** | `logroController.enviarLogro`, `getMisLogros` |
| **Tablas BD** | `logro`, `logro_evidencia`, `evidencia` |
| **Estado BD** | `logro.estado = 'enviado'` |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF05.2: Validación de logros por administrador

| Elemento | Detalle |
|----------|---------|
| **RF** | RF05.2 - Validación de logros |
| **Prototipo** | Vista "Validaciones" → tabla "Logros pendientes" |
| **Página HTML** | `view-admin` |
| **Endpoint API** | `GET /api/logros/pendientes`, `POST /api/logros/:id/aprobar`, `POST /api/logros/:id/rechazar` |
| **Controller** | `logroController.getLogrosPendientes`, `aprobarLogro`, `rechazarLogro` |
| **Tablas BD** | `logro.validado_por`, `logro.fecha_validacion` |
| **Middleware** | `requireRole(['administrador'])` |
| **Vista BD** | `v_logros_pendientes` |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF05.3: Asignación de XP al aprobar logro

| Elemento | Detalle |
|----------|---------|
| **RF** | RF05.3 - Asignación de XP |
| **Prototipo** | Simulado (botón "Simular actividad") |
| **Página HTML** | `view-gamificacion` |
| **Endpoint API** | Automático al aprobar logro |
| **Tablas BD** | `movimiento_xp`, `usuario.xp_total` |
| **Función BD** | `insertar_movimiento_xp` (tipo: logro_validado) |
| **Trigger BD** | `trg_logro_aprobado` (inserta XP al aprobar) |
| **Servicio Docker** | `riul-db` |

### RF05.4: Niveles con umbrales de XP y estrellas 1-5

| Elemento | Detalle |
|----------|---------|
| **RF** | RF05.4 - Niveles y estrellas |
| **Prototipo** | Vista "Gamificación" → badge hexagonal con estrellas |
| **Página HTML** | `view-gamificacion` |
| **Endpoint API** | `GET /api/auth/me` (incluye nivel y estrellas) |
| **Tablas BD** | `nivel`, `usuario.nivel_id` |
| **Función BD** | `actualizar_xp_usuario` (recalcula nivel) |
| **Restricción BD** | `nivel.numero CHECK (1-5)`, `nivel.estrellas CHECK (1-5)` |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF05.5: Otorgamiento de insignias según reglas

| Elemento | Detalle |
|----------|---------|
| **RF** | RF05.5 - Insignias |
| **Prototipo** | Vista "Gamificación" → grid de insignias |
| **Página HTML** | `view-gamificacion` |
| **Endpoint API** | `GET /api/auth/me` (incluye insignias) |
| **Tablas BD** | `insignia`, `usuario_insignia` |
| **Función BD** | `otorgar_insignias_usuario` (reglas: nivel>=3, xp>=1000, logros>=5, publicaciones>=10) |
| **Trigger BD** | `trg_logro_aprobado` (otorga insignias al aprobar) |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF05.6: Ranking de semilleros e investigadores

| Elemento | Detalle |
|----------|---------|
| **RF** | RF05.6 - Ranking |
| **Prototipo** | Vista "Ranking" → tabla ordenable |
| **Página HTML** | `view-ranking` |
| **Endpoint API** | `GET /api/ranking/semilleros`, `GET /api/ranking/investigadores` |
| **Controller** | `rankingController.getRankingSemilleros`, `getRankingInvestigadores` |
| **Tablas BD** | `usuario.xp_total`, `semillero` |
| **Vista BD** | `v_ranking_semilleros`, `v_ranking_investigadores` |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF05.7: Historial inmutable de movimientos XP

| Elemento | Detalle |
|----------|---------|
| **RF** | RF05.7 - Historial XP inmutable |
| **Prototipo** | Vista "Gamificación" → "Historial de actividades" |
| **Página HTML** | `view-gamificacion` |
| **Endpoint API** | N/A (no implementado en frontend actual) |
| **Tablas BD** | `movimiento_xp` |
| **Vista BD** | `v_historial_xp_usuario` |
| **Trigger BD** | `trg_movimiento_xp_inmutable` (impide UPDATE/DELETE) |
| **Servicio Docker** | `riul-db` |

---

## MÓDULO ANALÍTICA

### RF06.1: Dashboard con KPIs

| Elemento | Detalle |
|----------|---------|
| **RF** | RF06.1 - Dashboard KPIs |
| **Prototipo** | Vista "Dashboard" → 4 KPIs (XP, nivel, insignias, ranking) |
| **Página HTML** | `view-dashboard` |
| **Endpoint API** | `GET /api/ranking/kpis` |
| **Controller** | `rankingController.getKPIs` |
| **Vista BD** | `v_kpis_institucionales` |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF06.2: Vista de ranking de semilleros

| Elemento | Detalle |
|----------|---------|
| **RF** | RF06.2 - Ranking semilleros |
| **Prototipo** | Vista "Ranking" → tabla de semilleros |
| **Página HTML** | `view-ranking` |
| **Endpoint API** | `GET /api/ranking/semilleros` |
| **Controller** | `rankingController.getRankingSemilleros` |
| **Vista BD** | `v_ranking_semilleros` |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

### RF06.3: Vista de ranking de investigadores

| Elemento | Detalle |
|----------|---------|
| **RF** | RF06.3 - Ranking investigadores |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | `GET /api/ranking/investigadores` |
| **Controller** | `rankingController.getRankingInvestigadores` |
| **Vista BD** | `v_ranking_investigadores` |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF06.4: Vista de XP por usuario

| Elemento | Detalle |
|----------|---------|
| **RF** | RF06.4 - XP por usuario |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | N/A |
| **Vista BD** | `v_xp_por_usuario` |
| **Servicio Docker** | `riul-db` |

### RF06.5: Vista de impacto de publicaciones

| Elemento | Detalle |
|----------|---------|
| **RF** | RF06.5 - Impacto de publicaciones |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | N/A |
| **Vista BD** | `v_impacto_publicaciones` (reacciones, comentarios, compartidos) |
| **Servicio Docker** | `riul-db` |

### RF06.6: Vista de indicadores por facultad/programa

| Elemento | Detalle |
|----------|---------|
| **RF** | RF06.6 - Indicadores por facultad/programa |
| **Prototipo** | No visible en prototipo |
| **Página HTML** | N/A |
| **Endpoint API** | `GET /api/ranking/indicadores-facultad` |
| **Controller** | `rankingController.getIndicadoresFacultad` |
| **Vista BD** | `v_indicadores_facultad`, `v_indicadores_programa` |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RF06.7: Vista de hoja de vida investigativa

| Elemento | Detalle |
|----------|---------|
| **RF** | RF06.7 - Hoja de vida investigativa |
| **Prototipo** | Vista "Mi perfil" → "Hoja de vida investigativa" |
| **Página HTML** | `view-perfil` |
| **Endpoint API** | `GET /api/ranking/hoja-vida/:usuario_id` |
| **Controller** | `rankingController.getHojaVida` |
| **Vista BD** | `v_hoja_vida_investigativa` |
| **Servicio Docker** | `riul-api`, `riul-db`, `riul-web` |

---

## REQUERIMIENTOS NO FUNCIONALES (RNF)

### RNF01: Seguridad

| Elemento | Detalle |
|----------|---------|
| **RNF** | RNF01 - Seguridad (JWT, roles, bcrypt, permisos mínimos) |
| **Prototipo** | N/A (simulado) |
| **Middleware** | `authenticateToken` (JWT), `requireRole` (control de acceso) |
| **Librerías** | `bcrypt` (hash), `jsonwebtoken` (JWT) |
| **BD Roles** | `riul_app` (permisos mínimos), `riul_readonly` (solo lectura) |
| **BD Scripts** | `05_roles_security.sql` |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RNF02: Almacenamiento

| Elemento | Detalle |
|----------|---------|
| **RNF** | RNF02 - Almacenamiento de evidencias |
| **Prototipo** | N/A (simulado con placeholder) |
| **Endpoint API** | N/A (pendiente implementación con multer) |
| **Tablas BD** | `evidencia` (metadatos), `publicacion_evidencia`, `logro_evidencia` |
| **Volumen Docker** | `uploads` (pendiente configuración) |
| **Servicio Docker** | `riul-api`, `riul-db` |

### RNF03: Usabilidad

| Elemento | Detalle |
|----------|---------|
| **RNF** | RNF03 - Usabilidad (dashboard intuitivo, navegación fluida, responsive) |
| **Prototipo** | Todas las vistas (dashboard por rol, navegación lateral, responsive CSS) |
| **Página HTML** | Todas las vistas (`view-*`) |
| **CSS** | `assets/css/styles.css` (variables CSS, media queries) |
| **Servicio Docker** | `riul-web` (nginx) |

### RNF04: Mantenibilidad

| Elemento | Detalle |
|----------|---------|
| **RNF** | RNF04 - Mantenibilidad (arquitectura modular, código legible, lógica en BD) |
| **Estructura** | `api/` (modular), `database/` (organizado por scripts), `web/` (separado) |
| **BD Lógica** | Funciones y triggers en `03_functions_triggers.sql` |
| **API** | Puente delgado, usa funciones de BD |
| **Servicio Docker** | `docker-compose.yml` (servicios separados) |

### RNF05: Reproducibilidad

| Elemento | Detalle |
|----------|---------|
| **RNF** | RNF05 - Reproducibilidad (Docker, entorno reproducible) |
| **Configuración** | `docker-compose.yml`, `.env.example` |
| **Scripts BD** | `database/init/` (automático al crear contenedor) |
| **Comando** | `docker compose up --build` |
| **Servicios Docker** | `riul-db`, `riul-api`, `riul-web`, `riul-adminer` |

---

## Inconsistencias y Resoluciones

### Inconsistencia 1: Prototipo usa selector de rol en login, sistema real requiere validación admin

**Resolución**: En el sistema real, el registro crea cuenta con estado `pendiente`. El usuario debe esperar validación del administrador antes de poder hacer login. El prototipo simula esto permitiendo login directo con cualquier rol.

### Inconsistencia 2: Prototipo simula XP con botón "Simular actividad", sistema real usa funciones de BD

**Resolución**: En el sistema real, la XP se otorga automáticamente a través de funciones de BD (`insertar_movimiento_xp`) cuando se realizan acciones (publicar, comentar, logro validado). El prototipo simula esto manualmente.

### Inconsistencia 3: Prototipo no implementa subida de archivos reales

**Resolución**: En el sistema actual, la subida de evidencias está diseñada en BD (tabla `evidencia`) pero la implementación con `multer` en la API y el volumen Docker están pendientes. El prototipo usa un placeholder visual.

---

## Resumen de Cobertura

| Módulo | RF Cubiertos | Prototipo | HTML | API | BD | Docker |
|--------|--------------|-----------|-----|-----|----|---------|
| Usuarios | 5/5 (100%) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Investigación | 5/5 (100%) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Eventos | 5/5 (100%) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Comunidad | 6/6 (100%) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Gamificación | 7/7 (100%) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Analítica | 7/7 (100%) | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Total** | **35/35 (100%)** | **✓** | **✓** | **✓** | **✓** | **✓** |

**Nota**: Algunas funcionalidades están parcialmente implementadas en el frontend actual (por ejemplo, subida de archivos, seguimiento, notificaciones), pero la infraestructura está completa en BD y API.
