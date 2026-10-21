# RIUL - Red de Investigación Universidad Libre

Segundo corte de la plataforma institucional para conectar a quienes investigan en la Universidad Libre (semilleros, proyectos, publicaciones, eventos, convocatorias, logros y gamificación).

## 📋 Índice

- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Credenciales de Demo](#credenciales-de-demo)
- [URLs de Acceso](#urls-de-acceso)
- [Decisiónes Técnicas](#decisiones-técnicas)
- [Documentación](#documentación)

---

## Requisitos

- **Docker** y **Docker Compose** instalados
- **Node.js** 20+ (para desarrollo local, opcional)
- **PostgreSQL** 16+ (para desarrollo local, opcional)

---

## Estructura del Proyecto

```
riul/
├── docker-compose.yml          # Orquestación de servicios Docker
├── .env.example               # Variables de entorno (plantilla)
├── .gitignore                 # Archivos ignorados por Git
├── README.md                  # Este archivo
├── database/                  # Base de datos
│   ├── init/
│   │   ├── 01_extensions_types.sql   # Extensiones, ENUMs, catálogos
│   │   ├── 02_schema.sql             # Tablas, PK, FK, índices
│   │   ├── 03_functions_triggers.sql # Lógica de negocio en BD
│   │   ├── 04_views.sql              # Vistas de analítica
│   │   ├── 05_roles_security.sql     # Roles y permisos de BD
│   │   └── 06_seed.sql               # Datos semilla
│   ├── tests/
│   │   └── verify.sql                # Script de pruebas
│   ├── ER_diagram.md             # Diagrama ER en Mermaid
│   ├── diccionario_de_datos.md   # Diccionario de datos completo
│   └── README_db.md              # Documentación de la BD
├── api/                       # Backend (Node.js + Express)
│   ├── Dockerfile               # Multi-stage build
│   ├── package.json            # Dependencias
│   └── src/
│       ├── config/
│       │   └── database.js      # Configuración de PostgreSQL
│       ├── middleware/
│       │   └── auth.js         # Autenticación JWT y roles
│       ├── controllers/
│       │   ├── authController.js
│       │   ├── publicacionController.js
│       │   ├── semilleroController.js
│       │   ├── logroController.js
│       │   ├── adminController.js
│       │   └── rankingController.js
│       ├── routes/
│       │   ├── auth.js
│       │   ├── publicaciones.js
│       │   ├── semilleros.js
│       │   ├── logros.js
│       │   ├── admin.js
│       │   └── ranking.js
│       └── server.js            # Punto de entrada
├── web/                       # Frontend (HTML + CSS + JS vanilla)
│   ├── Dockerfile               # Build con nginx
│   ├── nginx/
│   │   └── default.conf         # Configuración nginx
│   └── public/
│       ├── index.html           # Página principal
│       ├── assets/
│       │   ├── css/
│       │   │   └── styles.css   # Estilos del prototipo
│       │   └── js/
│       │       ├── api.js        # Cliente fetch
│       │       └── app.js       # Lógica de aplicación
└── docs/                      # Documentación
    ├── entrada/
    │   ├── prototipo/           # Prototipo del primer corte
    │   ├── Descripcion_del_proyecto_RIUL.docx
    │   └── RIUL WORKFLOW.pdf
    ├── trazabilidad.md          # Matriz RF → Prototipo → HTML → API → BD → Docker
    └── INVENTARIO.md            # Inventario completo del proyecto
```

---

## Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd riul
```

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Editar `.env` si deseas cambiar las contraseñas (opcional para desarrollo):

```env
DB_PASSWORD=riul_dev_password
JWT_SECRET=riul_jwt_secret_dev
PORT=3000
```

### 3. Levantar los Servicios con Docker

```bash
docker compose up --build
```

Este comando:
- Construye las imágenes Docker de la API y el frontend
- Levanta PostgreSQL y ejecuta los scripts de inicialización (`database/init/`)
- Levanta la API Node.js (espera a que la BD esté healthy)
- Levanta nginx sirviendo el frontend y haciendo proxy a la API
- Levanta Adminer para inspeccionar la BD

### 4. Verificar que los Servicios Estén Healthy

```bash
docker compose ps
```

Deberías ver todos los servicios con estado `Up` o `healthy`.

### 5. Acceder a la Aplicación

- **Frontend**: http://localhost:8080
- **Adminer (BD)**: http://localhost:8081
- **API**: http://localhost:3000 (directo, o vía nginx: http://localhost:8080/api)

---

## Credenciales de Demo

Las contraseñas están hasheadas con bcrypt para `Password123!`.

### Administrador

- **Email**: `admin@unilibre.edu.co`
- **Contraseña**: `Password123!`
- **Rol**: Administrador
- **Permisos**: Validar cuentas, validar logros, CRUD de entidades

### Docente Líder (semillero RIUL-Dev)

- **Email**: `docente1@unilibre.edu.co`
- **Contraseña**: `Password123!`
- **Rol**: Docente líder
- **Permisos**: Gestionar semillero, aprobar vinculaciones

### Estudiante

- **Email**: `estudiante1@unilibre.edu.co`
- **Contraseña**: `Password123!`
- **Rol**: Estudiante investigador
- **Permisos**: Explorar, publicar, comentar, enviar logros

### Cuentas Pendientes de Validación

- `ana.martinez@unilibre.edu.co` (Pendiente)
- `juan.torres@unilibre.edu.co` (Pendiente)

---

## URLs de Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:8080 | Aplicación web principal |
| **API Health** | http://localhost:8080/api/health | Health check de la API |
| **Adminer** | http://localhost:8081 | Interfaz web para PostgreSQL |
| **PostgreSQL** | localhost:5432 | Puerto directo de la BD |

---

## Comandos Útiles

### Reiniciar la Base de Datos desde Cero

```bash
docker compose down -v
docker compose up --build
```

**Advertencia**: Esto borra todos los datos, incluyendo los datos semilla.

### Ver Logs de un Servicio

```bash
# API
docker compose logs -f api

# Base de datos
docker compose logs -f db

# Frontend (nginx)
docker compose logs -f web
```

### Entrar al Contenedor de PostgreSQL

```bash
docker exec -it riul-db psql -U riul_app -d riul
```

### Ejecutar Script de Pruebas de BD

```bash
docker exec -it riul-db psql -U riul_app -d riul -f /docker-entrypoint-initdb.d/../tests/verify.sql
```

### Backup de la Base de Datos

```bash
docker exec riul-db pg_dump -U riul_app riul > backup.sql
```

### Restaurar Backup

```bash
docker exec -i riul-db psql -U riul_app riul < backup.sql
```

### Detener Servicios

```bash
docker compose down
```

---

## Decisiones Técnicas

### 1. Base de Datos en Docker (Prioridad Absoluta)

**Decisión**: La base de datos es el componente más importante del proyecto. Está completa, normalizada (3FN), robusta y bien documentada.

**Justificación**:
- Toda la lógica de negocio crítica (XP, niveles, vinculaciones) está implementada en la BD con funciones y triggers
- Esto asegura integridad de datos y rendimiento
- La API es un puente delgado que delega lógica a la BD

### 2. PK SERIAL vs UUID

**Decisión**: Usamos `SERIAL` (IDENTITY) para todas las PKs.

**Justificación**:
- Simplicidad y performance
- Suficiente para el escalado esperado
- Compatible con herramientas de visualización

### 3. Borrado Lógico

**Decisión**: Tablas principales tienen `eliminado_en` para borrado lógico.

**Justificación**:
- Preservar historial de investigaciones
- Permitir recuperación de datos
- Mantener integridad referencial

### 4. XP Total y Nivel Mantenidos por Trigger

**Decisión**: `usuario.xp_total` y `usuario.nivel_id` se actualizan automáticamente por triggers.

**Justificación**:
- Performance: Evitar cálculos repetitivos de SUM()
- Facilita ranking y consultas frecuentes
- El valor "verdadero" sigue en `movimiento_xp`

### 5. Movimiento XP Inmutable

**Decisión**: `movimiento_xp` es inmutable (trigger impide UPDATE/DELETE).

**Justificación**:
- Integridad del historial de XP
- Auditoría y trazabilidad
- Evitar manipulación de puntos

### 6. Stack Tecnológico Obligatorio

**Decisión**: Sin frameworks (React/Vue/Angular), sin ORM, solo tecnologías especificadas.

**Justificación**:
- Requisito académico del proyecto
- Mantener simplicidad y control total
- Demostrar conocimientos fundamentales

### 7. Frontend Vanilla (HTML + CSS + JS)

**Decisión**: Sin frameworks frontend, solo ES modules y fetch.

**Justificación**:
- Requisito del proyecto
- Ligero y rápido
- Fácil de entender y mantener

### 8. API REST como Puente Delgado

**Decisión**: La API no reimplementa lógica de negocio, usa funciones de la BD.

**Justificación**:
- Single source of truth en la BD
- Consistencia entre diferentes clientes
- Menos código duplicado

### 9. Docker Multi-Service

**Decisión**: 4 servicios separados (db, api, web, adminer).

**Justificación**:
- Reproducibilidad exacta del entorno
- Escalabilidad independiente
- Aislamiento de dependencias

### 10. Seguridad por Roles en BD

**Decisión**: Roles de BD (`riul_app`, `riul_readonly`) con permisos mínimos.

**Justificación**:
- Defense in depth
- Minimizar impacto de compromisos
- Separación de responsabilidades

---

## Documentación

### Base de Datos

- **README_db.md**: Decisiones de diseño, normalización, conexión, reinicio
- **ER_diagram.md**: Diagrama entidad-relación completo en Mermaid
- **diccionario_de_datos.md**: Descripción detallada de cada tabla y atributo
- **verify.sql**: Script que prueba restricciones, triggers y vistas

### Documentación del Proyecto

- **INVENTARIO.md**: Inventario completo de módulos, pantallas, roles, flujos y requerimientos
- **trazabilidad.md**: Matriz RF → Prototipo → HTML → API → BD → Docker
- **docs/entrada/**: Documentos originales (descripción, workflow, prototipo)

---

## Verificación del Corte

### Criterios de Aceptación

- [x] `docker compose up --build` levanta los 4 servicios en estado healthy
- [x] La BD se crea sola con tablas, funciones, triggers, vistas, roles y seed
- [x] `database/tests/verify.sql` demuestra restricciones, triggers y vistas
- [x] Modelo en 3FN, todas las FK/PK/índices definidos
- [x] ER Mermaid renderiza y el diccionario cubre el 100% de las tablas
- [x] El flujo completo de punta a punta funciona en el navegador
- [x] Cada módulo del prototipo tiene página, endpoints y tablas
- [x] La matriz de trazabilidad está completa
- [x] README con requisitos, comandos, URLs, credenciales de demo

### Flujo Completo de Punta a Punta

1. **Registro**: Usuario se registra → Cuenta en estado `pendiente`
2. **Validación**: Admin aprueba cuenta → Estado cambia a `aprobada` → XP otorgada
3. **Login**: Usuario hace login → Token JWT → Dashboard según rol
4. **Vinculación**: Estudiante solicita vinculación a semillero → Docente aprueba → XP otorgada
5. **Publicación**: Usuario crea publicación → XP otorgada → Notificación a seguidores
6. **Logro**: Usuario envía logro → Admin aprueba → XP otorgada → Nivel sube → Insignias otorgadas
7. **Ranking**: Ranking se actualiza automáticamente con cada movimiento XP

---

## Limitaciones Conocidas

1. **Subida de archivos**: La infraestructura para evidencias está diseñada en BD (tabla `evidencia`) pero la implementación con `multer` en la API y el volumen Docker están pendientes.
2. **Notificaciones en frontend**: El icono de campana existe pero no muestra notificaciones en tiempo real (las notificaciones se crean en BD correctamente).
3. **Seguimiento**: La funcionalidad de follow entre usuarios/semilleros está diseñada en BD pero no implementada en el frontend.
4. **Responsive**: El CSS del prototipo tiene media queries pero no ha sido testeado exhaustivamente en móviles.

---

## Próximos Pasos Sugeridos

1. Implementar subida de archivos con `multer` y volumen Docker
2. Implementar endpoint de notificaciones en frontend
3. Implementar funcionalidad de seguimiento (follow)
4. Agregar más pruebas unitarias y de integración
5. Implementar CI/CD para despliegue automatizado

---

## Contacto

Para preguntas sobre el proyecto, consulte:
- Documentación de la BD: `database/README_db.md`
- Matriz de trazabilidad: `docs/trazabilidad.md`
- Inventario del proyecto: `docs/INVENTARIO.md`
