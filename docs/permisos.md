# Matriz de Permisos por Rol - RIUL

## Roles del Sistema

| Rol | Descripción |
|-----|-------------|
| `administrador` | Administrador del sistema con acceso completo |
| `docente` | Docente líder de semillero |
| `estudiante` | Estudiante investigador |
| `visitante` | Visitante con solo lectura pública |

## Matriz de Permisos

### Autenticación y Usuarios

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/auth/register` | POST | ✅ | ✅ | ✅ | ✅ |
| `/api/auth/login` | POST | ✅ | ✅ | ✅ | ✅ |
| `/api/auth/me` | GET | ✅ | ✅ | ✅ | ❌ |
| `/api/usuarios` | GET | ✅ | ❌ | ❌ | ❌ |
| `/api/usuarios/{id}` | GET | ✅ | ❌ | ❌ | ❌ |
| `/api/usuarios/{id}` | PUT | ✅ | ❌ | ✅ (solo propio) | ❌ |
| `/api/usuarios/{id}` | DELETE | ✅ | ❌ | ❌ | ❌ |
| `/api/usuarios/{id}/aprobar` | PATCH | ✅ | ❌ | ❌ | ❌ |
| `/api/usuarios/{id}/rechazar` | PATCH | ✅ | ❌ | ❌ | ❌ |

### Catálogos

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/facultades` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/programas` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/lineas-investigacion` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/categorias-publicacion` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/tipos-actividad-xp` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/niveles` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/insignias` | GET | ✅ | ✅ | ✅ | ✅ |
| **CRUD catálogos** | POST/PUT/DELETE | ✅ | ❌ | ❌ | ❌ |

### Semilleros

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/semilleros` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/semilleros/{id}` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/semilleros` | POST | ✅ | ✅ | ❌ | ❌ |
| `/api/semilleros/{id}` | PUT | ✅ | ✅ (solo si líder) | ❌ | ❌ |
| `/api/semilleros/{id}` | DELETE | ✅ | ✅ (solo si líder) | ❌ | ❌ |
| `/api/semilleros/{id}/solicitar` | POST | ❌ | ❌ | ✅ | ❌ |
| `/api/semilleros/{id}/integrantes` | GET | ✅ | ✅ (solo si líder) | ✅ | ❌ |
| `/api/vinculaciones/{id}/resolver` | PATCH | ✅ | ✅ (solo si líder del semillero) | ❌ | ❌ |

### Proyectos

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/proyectos` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/proyectos/{id}` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/proyectos` | POST | ✅ | ✅ | ❌ | ❌ |
| `/api/proyectos/{id}` | PUT | ✅ | ✅ (solo integrante) | ❌ | ❌ |
| `/api/proyectos/{id}` | DELETE | ✅ | ✅ (solo integrante) | ❌ | ❌ |
| `/api/proyectos/{id}/avances` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/proyectos/{id}/avances` | POST | ✅ | ✅ (solo integrante) | ❌ | ❌ |
| `/api/proyectos/{id}/productos` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/proyectos/{id}/productos` | POST | ✅ | ✅ (solo integrante) | ❌ | ❌ |

### Eventos

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/eventos` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/eventos/{id}` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/eventos` | POST | ✅ | ✅ | ❌ | ❌ |
| `/api/eventos/{id}` | PUT | ✅ | ✅ (solo creador) | ❌ | ❌ |
| `/api/eventos/{id}` | DELETE | ✅ | ✅ (solo creador) | ❌ | ❌ |
| `/api/eventos/{id}/participar` | POST | ✅ | ✅ | ✅ | ❌ |

### Convocatorias

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/convocatorias` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/convocatorias/{id}` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/convocatorias` | POST | ✅ | ❌ | ❌ | ❌ |
| `/api/convocatorias/{id}` | PUT | ✅ | ❌ | ❌ | ❌ |
| `/api/convocatorias/{id}/validar` | PATCH | ✅ | ❌ | ❌ | ❌ |
| `/api/convocatorias/{id}/postular` | POST | ❌ | ✅ | ✅ | ❌ |
| `/api/postulaciones` | GET | ✅ | ❌ | ❌ | ❌ |
| `/api/postulaciones/{id}/resolver` | PATCH | ✅ | ❌ | ❌ | ❌ |

### Comunidad (Publicaciones)

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/publicaciones` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/publicaciones/{id}` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/publicaciones` | POST | ✅ | ✅ | ✅ | ❌ |
| `/api/publicaciones/{id}` | PUT | ✅ | ✅ (solo autor) | ✅ (solo autor) | ❌ |
| `/api/publicaciones/{id}` | DELETE | ✅ | ✅ (solo autor) | ✅ (solo autor) | ❌ |
| `/api/publicaciones/{id}/comentarios` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/publicaciones/{id}/comentarios` | POST | ✅ | ✅ | ✅ | ❌ |
| `/api/publicaciones/{id}/reacciones` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/publicaciones/{id}/reacciones` | POST | ✅ | ✅ | ✅ | ❌ |
| `/api/publicaciones/{id}/compartir` | POST | ✅ | ✅ | ✅ | ❌ |

### Notificaciones

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/notificaciones` | GET | ✅ | ✅ | ✅ | ❌ |
| `/api/notificaciones/{id}` | PATCH | ✅ | ✅ (solo propia) | ✅ (solo propia) | ❌ |

### Logros y Gamificación

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/gamificacion/me` | GET | ✅ | ✅ | ✅ | ❌ |
| `/api/logros` | GET | ✅ | ✅ | ✅ | ❌ |
| `/api/logros` | POST | ✅ | ✅ | ✅ | ❌ |
| `/api/logros/pendientes` | GET | ✅ | ❌ | ❌ | ❌ |
| `/api/logros/{id}/validar` | PATCH | ✅ | ❌ | ❌ | ❌ |
| `/api/logros/{id}/rechazar` | PATCH | ✅ | ❌ | ❌ | ❌ |

### Analítica

| Endpoint | Método | admin | docente | estudiante | visitante |
|----------|--------|-------|---------|------------|-----------|
| `/api/ranking/se milleros` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/ranking/investigadores` | GET | ✅ | ✅ | ✅ | ✅ |
| `/api/kpis` | GET | ✅ | ✅ | ❌ | ❌ |
| `/api/indicadores/facultad` | GET | ✅ | ✅ | ❌ | ❌ |
| `/api/hoja-vida/{id}` | GET | ✅ | ✅ | ✅ (solo propia) | ❌ |

## Reglas de Negocio Adicionales

1. **Validación de cuentas**: Un usuario con estado `pendiente` no puede iniciar sesión. Solo un administrador puede aprobar/rechazar cuentas.

2. **Vinculación a semillero**: 
   - Solo un docente líder del semillero (o un administrador) puede resolver solicitudes de vinculación.
   - Un estudiante no puede solicitar vinculación a un semillero donde ya es integrante.

3. **Postulación a convocatoria**:
   - Solo mientras la convocatoria esté abierta (estado `publicada` y fecha actual entre apertura y cierre).
   - Un usuario solo puede postular una vez por convocatoria.
   - Solo un administrador puede resolver postulaciones.

4. **Logros**:
   - Cualquier usuario puede enviar logros.
   - Solo un administrador puede validar/rechazar logros.
   - Al validar un logro, se otorga XP, se actualiza el nivel y se otorgan insignias si corresponde.

5. **Edición de recursos**:
   - Un usuario solo puede editar recursos que él mismo creó (publicaciones, eventos, proyectos).
   - Un docente líder puede editar semilleros que lidera.
   - Un administrador puede editar cualquier recurso.

6. **XP y Niveles**:
   - El XP se calcula automáticamente según la tabla `tipo_actividad_xp`.
   - El nivel se actualiza automáticamente cuando el XP cruza los umbrales definidos en la tabla `nivel`.
