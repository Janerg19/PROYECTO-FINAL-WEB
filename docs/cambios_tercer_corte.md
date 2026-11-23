# Cambios del Tercer Corte - RIUL

## Decisión Estratégica: Mantener PostgreSQL

### Justificación para no migrar a MySQL

El proyecto original del segundo corte fue diseñado y desarrollado completamente con **PostgreSQL 16**. Después de evaluar los costos y beneficios de migrar a MySQL 8.0, se decidió **mantener PostgreSQL** por las siguientes razones:

1. **Modelo de datos ya implementado y probado**: Las 35 tablas, funciones, triggers y vistas están completamente implementadas en PostgreSQL. Migrarlas implicaría reescribir toda la lógica de negocio que está en PL/pgSQL.

2. **Funcionalidades avanzadas de PostgreSQL necesarias**:
   - Arrays (`text[]`) para intereses de investigación (MySQL requiere JSON, menos idiomático)
   - ENUMs nativos con mejor validación
   - Triggers y funciones PL/pgSQL más potentes para lógica de negocio
   - Vistas materializadas y avanzadas para analítica
   - Índices parciales (WHERE conditions)
   - FULL TEXT SEARCH nativo para búsqueda en publicaciones

3. **Portabilidad sin pérdida**: PostgreSQL es compatible con SQLAlchemy ORM y cumple con todos los requisitos de la rúbrica (conexión BD, ORM, CRUD, etc.). La rúbrica permite justificar el stack tecnológico si se demuestra su idoneidad.

4. **Rendimiento y madurez**: PostgreSQL es más maduro en características de analítica y consultas complejas, críticas para las vistas de ranking y KPIs del proyecto.

5. **Time-to-market**: Mantener PostgreSQL permite enfocar el esfuerzo en los objetivos principales del tercer corte (arquitectura modular, API REST completa, reglas de negocio, seguridad, pruebas) en lugar de perder tiempo en una migración compleja que no añade valor funcional.

### Stack Tecnológico Final

- **Backend**: Python 3.12 + Flask 3 + SQLAlchemy 2.x + Flask-SQLAlchemy
- **Base de Datos**: PostgreSQL 16 (mantenido del corte 2)
- **ORM**: SQLAlchemy con modelos declarativos
- **Validación/Serialización**: marshmallow
- **Seguridad**: Flask-JWT-Extended + bcrypt
- **Documentación**: flasgger (Swagger/OpenAPI)
- **Servidor de producción**: gunicorn
- **Tests**: pytest
- **Frontend**: HTML + CSS + JavaScript vanilla (sin cambios)
- **Orquestación**: Docker + Docker Compose

## Cambios Realizados

### 1. Arquitectura Modular del Backend

Se reorganizó el backend siguiendo el patrón MVC con separación de responsabilidades:

```
api/
├── Dockerfile
├── requirements.txt
├── wsgi.py
└── app/
    ├── __init__.py              # Application factory
    ├── config.py                # Configuración por entorno
    ├── extensions.py            # db, jwt, cors, swagger
    ├── models/                  # Modelos SQLAlchemy por módulo
    │   ├── usuarios.py
    │   ├── investigacion.py
    │   ├── eventos.py
    │   ├── comunidad.py
    │   └── gamificacion.py
    ├── schemas/                 # Marshmallow schemas
    │   ├── usuarios.py
    │   ├── investigacion.py
    │   ├── eventos.py
    │   ├── comunidad.py
    │   └── gamificacion.py
    ├── routes/                  # Blueprints Flask
    │   ├── usuarios.py
    │   ├── investigacion.py
    │   ├── eventos.py
    │   ├── comunidad.py
    │   └── gamificacion.py
    ├── controllers/             # Manejo HTTP
    │   ├── usuarios.py
    │   ├── investigacion.py
    │   ├── eventos.py
    │   ├── comunidad.py
    │   └── gamificacion.py
    ├── services/                # REGLAS DE NEGOCIO
    │   ├── usuarios.py
    │   ├── investigacion.py
    │   ├── eventos.py
    │   ├── comunidad.py
    │   └── gamificacion.py
    ├── middleware/              # Autenticación y roles
    │   ├── auth.py
    │   └── errors.py
    └── utils/                   # Helpers
        ├── errors.py
        └── pagination.py
```

**Principios aplicados:**
- Controladores delgados: solo manejan request/response
- Servicios contienen toda la lógica de negocio
- Modelos SQLAlchemy representan 1:1 las tablas de la BD
- Schemas marshmallow para validación y serialización
- Separación clara entre capas

### 2. Migración a SQLAlchemy ORM

Se crearon modelos SQLAlchemy para las 35 tablas:
- Atributos con tipos correctos (Integer, String, Text, DateTime, Boolean, etc.)
- Primary Keys y Foreign Keys definidas
- `relationship()` con `back_populates` para navegación ORM
- `__tablename__` coincide con nombres de tablas
- Índices definidos en modelos con `index=True`
- Borrado lógico con `eliminado_en` donde aplica

### 3. API REST Completa con CRUD

Se implementaron endpoints GET, POST, PUT, PATCH, DELETE para:
- **Usuarios**: auth (register, login, me), CRUD usuarios, aprobar/rechazar cuentas
- **Catálogos**: facultades, programas, líneas, categorías, tipos XP, niveles, insignias
- **Investigación**: semilleros, integrantes, proyectos, avances, productos
- **Eventos**: eventos, participaciones
- **Convocatorias**: CRUD convocatorias, postulaciones (postular, aprobar, rechazar)
- **Comunidad**: publicaciones, comentarios, reacciones, compartidos, seguimientos, notificaciones, evidencias
- **Gamificación**: logros, XP, niveles, insignias, historial
- **Analítica**: ranking semilleros/investigadores, KPIs, indicadores facultad, hoja de vida

Códigos HTTP correctos: 200, 201, 204, 400, 401, 403, 404, 409, 422.

### 4. Reglas de Negocio en Services/

La lógica de negocio de PostgreSQL triggers se migró a la capa de servicios en Python:
- Validación de cuentas: pendiente → aprobada (no puede login hasta aprobación)
- Vinculación a semillero: solicitud → aprobación/rechazo por docente líder
- Postulación a convocatoria: validación de fechas, una por usuario
- **Gamificación**: Publicar (+80 XP), comentar (+20), reaccionar (+10), proyecto (+150), producto (+200), evento (+40), vinculación (+100), cuenta validada (+50), logro aprobado (+300)
- Cálculo de nivel según umbrales XP (1, 500, 1000, 2000, 4000)
- Otorgamiento de insignias según reglas
- Todo en transacciones atómicas

### 5. Seguridad y Permisos

- JWT con Flask-JWT-Extended (expiración configurable)
- Contraseñas con bcrypt
- Decorador `@roles_required(['administrador', 'docente', 'estudiante'])`
- Matriz de permisos documentada en `docs/permisos.md`
- CORS configurado
- Secretos en variables de entorno (.env)
- Validación de inputs con marshmallow

### 6. Swagger/OpenAPI

Implementado con flasgger:
- UI en `/api/docs`
- Especificación en `/api/openapi.json`
- Cada endpoint documentado con: resumen, parámetros, body schema, respuestas
- Seguridad Bearer JWT con botón "Authorize"

### 7. Pruebas

- pytest con casos de:
  - CRUD exitoso
  - Errores (400, 401, 403, 404, 409, 422)
  - Permisos por rol
  - Reglas de negocio (flujo logro, vinculación, XP)
- Colección Postman en `docs/postman/`
- `docs/pruebas.md` con evidencias

### 8. Correcciones del Seed

Se corrigieron errores en `database/init/06_seed.sql`:
- **Roles**: admin@unilibre.edu.co → administrador, docente1/2/3@ → docente, estudiantes → estudiante (usando SELECT id FROM rol WHERE nombre = '...')
- **XP coherente**: usuario.xp_total coincide con SUM(movimiento_xp.xp_ganada)
- **Niveles**: usuario.nivel_id corresponde a umbrales de XP
- **Fechas_resolucion**: postulaciones aprobadas/rechazadas tienen fecha y revisado_por
- **Referencias**: validado_por/revisado_por apuntan a usuarios con rol correcto

### 9. Correcciones del Frontend

- **Gamificación**: Conectado a `GET /api/gamification/me` (XP, nivel, estrellas, insignias, historial reales)
- **Perfil**: Carga datos del usuario autenticado
- **Publicaciones**: Categorías dinámicas, subida de evidencias real, comentar/reaccionar funcionales
- **Semilleros**: Solicitar vinculación, docente ve solicitudes pendientes
- **Eventos/Convocatorias**: Listas dinámicas, postular, admin aprueba/rechaza postulaciones
- **Notificaciones**: Lista de notificaciones funcionales

### 10. Docker

- db: PostgreSQL 16 con healthcheck
- api: Python 3.12-slim con gunicorn, espera a BD healthy
- web: nginx con proxy /api y /api/docs
- adminer: compatible con PostgreSQL
- Volúmenes: pgdata, uploads

## Verificación Final

- ✅ `docker compose down -v && docker compose up --build` levanta servicios sanos
- ✅ Seed sin errores, roles correctos (admin=administrador, docentes=docente)
- ✅ Modelos SQLAlchemy coinciden con esquema (prueba automática)
- ✅ Swagger UI en `/api/docs` con todos los endpoints
- ✅ pytest en verde
- ✅ Colección Postman incluida
- ✅ Frontend sin datos fijos, todo desde API
- ✅ Documentación consistente (sin referencias a Node.js)

## Criterios de Rúbrica Cumplidos

1. **Arquitectura y estructura**: ✅ Modular con separación routes/controllers/services/models/config
2. **Conexión e integración BD**: ✅ Flask + PostgreSQL + SQLAlchemy, modelos = entidades
3. **API REST y CRUD**: ✅ GET/POST/PUT/PATCH/DELETE, códigos HTTP correctos, Swagger
4. **Lógica de negocio y seguridad**: ✅ Reglas en services/, validación marshmallow, JWT + roles
5. **Pruebas y funcionamiento**: ✅ pytest + Postman, Docker funcional
6. **Coherencia e integración**: ✅ Correspondencia RF → BD → API → Frontend documentada
