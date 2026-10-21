# INVENTARIO DE RIUL - SEGUNDO CORTE

Este documento inventaria todos los elementos del proyecto basado en los insumos:
- Descripción del proyecto RIUL.docx
- RIUL WORKFLOW.pdf
- Prototipo funcional (HTML/CSS/JS)

---

## 1. MÓDULOS FUNCIONALES

### 1.1 Módulo Usuarios
**Objetivo:** Gestión de cuentas, roles y perfiles investigativos.

**Elementos:**
- Login con rol de demo (estudiante, docente líder, administrador)
- Registro de nueva cuenta institucional
- Validación administrativa de cuentas (pendiente/aprobada/rechazada/suspendida)
- Perfil de usuario con hoja de vida investigativa
- Configuración de facultad y programa académico
- Gestión de roles: estudiante investigador, docente líder, administrador, visitante

**Flujos:**
1. Registro → Pendiente validación → Aprobación admin → Cuenta activa
2. Login → Dashboard según rol
3. Actualización de perfil

---

### 1.2 Módulo Investigación
**Objetivo:** Administración de semilleros, proyectos, productos y líneas de investigación.

**Elementos:**
- Semilleros (gestión por docente líder)
- Líneas de investigación
- Integrantes de semillero (N:M con estado: solicitada/aprobada/rechazada/retirada)
- Proyectos de investigación
- Avances de proyectos
- Productos (artículos, ponencias, patentes, software, etc.)
- Tipos de producto

**Flujos:**
1. Estudiante explora semilleros → Solicita vinculación → Docente aprueba/rechaza
2. Docente gestiona integrantes, registra proyectos y avances
3. Proyectos tienen avances y productos asociados

---

### 1.3 Módulo Eventos y Convocatorias
**Objetivo:** Agenda académica y oportunidades de financiación.

**Elementos:**
- Eventos (coloquios, talleres, ferias)
- Participación en eventos
- Convocatorias (con estado y validación administrativa)
- Postulaciones a convocatorias

**Flujos:**
1. Usuario consulta eventos
2. Usuario postula a convocatoria
3. Administrador valida convocatorias

---

### 1.4 Módulo Comunidad
**Objetivo:** Interacción social y difusión de avances.

**Elementos:**
- Categorías de publicación
- Publicaciones (feed social)
- Evidencias (archivos adjuntos con metadatos)
- Comentarios en publicaciones
- Reacciones (UNIQUE usuario+publicación+tipo)
- Compartidos
- Seguimiento (follow entre usuarios/semilleros)
- Notificaciones

**Flujos:**
1. Usuario crea publicación con categoría y evidencias
2. Otros usuarios reaccionan, comentan, comparten
3. Sistema genera notificaciones de interacción

---

### 1.5 Módulo Gamificación
**Objetivo:** Reconocimiento mediante XP, niveles, insignias y ranking.

**Elementos:**
- Tipos de actividad con XP base
- Logros (enviado/aprobado/rechazado, con validador y fecha de validación)
- Movimientos de XP (historial inmutable)
- Niveles (umbral de XP, estrellas 1-5)
- Insignias
- Usuario-insignia (otorgamiento)
- Ranking de semilleros
- Ranking de investigadores

**Flujos:**
1. Usuario envía logro con evidencia
2. Administrador aprueba logro → Sistema inserta movimiento XP → Recalcula total
3. Si supera umbral → Sube de nivel/estrellas → Otorga insignias según reglas
4. Ranking se actualiza automáticamente

---

### 1.6 Módulo Analítica
**Objetivo:** Indicadores institucionales y reportes.

**Elementos:**
- Dashboard con KPIs
- Vista de ranking de semilleros
- Vista de ranking de investigadores
- Vista de XP por usuario
- Vista de impacto de publicaciones (reacciones, comentarios, compartidos)
- Vista de indicadores institucionales (por facultad/programa)
- Vista de hoja de vida investigativa

---

## 2. PANTALLAS DEL PROTOTIPO

### 2.1 Pantallas Públicas
1. **Landing page** (view-login):
   - Hero con estadísticas (32 semilleros, 1,204 publicaciones, 410 logros)
   - Panel de login
   - Registro de nueva cuenta

### 2.2 Pantallas por Rol

#### Estudiante Investigador
1. **Dashboard** (view-dashboard):
   - KPIs: XP total, Nivel actual, Insignias, Ranking del semillero
   - Publicaciones recientes
   - Próximos eventos
   - Convocatoria abierta

2. **Mi perfil** (view-perfil):
   - Información del usuario (nombre, programa, semillero)
   - Estrellas de nivel
   - Barra de progreso de XP
   - Formulario "Registrar nuevo logro"
   - Hoja de vida investigativa (artículos, ponencias, proyectos, eventos, patentes)
   - Logros pendientes de validación

3. **Publicaciones** (view-publicaciones):
   - Feed completo de publicaciones
   - Botón "Crear publicación" (modal)
   - Categorías: Logro, Proyecto, Evento, General
   - Evidencias adjuntas
   - Reacciones, comentarios, compartir

4. **Eventos y convocatorias** (view-eventos):
   - Lista de próximos eventos
   - Lista de convocatorias abiertas
   - Botón "Postularse"

5. **Gamificación** (view-gamificacion):
   - Badge de nivel con hexágono
   - Estrellas
   - Barra de progreso de XP
   - Botón "Simular nueva actividad"
   - Grid de insignias (8 slots, 6 activas)
   - Historial de actividades

6. **Ranking** (view-ranking):
   - KPIs institucionales (semilleros activos, publicaciones, proyectos, logros)
   - Tabla ranking de semilleros (ordenable por: posición, nombre, facultad, XP, nivel)

#### Docente Líder
Todas las pantallas de estudiante +:

7. **Gestión de semillero** (view-semillero):
   - Información del semillero
   - Lista de integrantes con roles (Líder, Estudiante)
   - Botón "Agregar" integrante
   - Lista de proyectos del semillero
   - Botón "+ Nuevo" proyecto
   - Validación de participación (enlace a admin)

#### Administrador
Todas las pantallas anteriores +:

8. **Validaciones** (view-admin):
   - Tabla de cuentas pendientes (nombre, correo, rol, documento, acciones aprobar/rechazar)
   - Tabla de logros pendientes (estudiante, tipo, descripción, acciones aprobar/rechazar)

#### Visitante
Solo lectura:
- Dashboard
- Publicaciones (sin botón crear)
- Eventos y convocatorias
- Ranking

---

## 3. ROLES Y PERMISOS

| Rol | Permisos |
|-----|----------|
| **Estudiante investigador** | Explorar semilleros, solicitar vinculación, registrar logros, crear publicaciones, comentar, reaccionar, ver perfil/gamificación/ranking |
| **Docente líder** | Todo lo de estudiante + gestionar semillero, aprobar/rechazar vinculaciones, registrar proyectos/avances/productos |
| **Administrador** | Todo lo anterior + validar cuentas, validar logros, gestionar facultades/programas/semilleros/convocatorias, ver reportes |
| **Visitante** | Solo lectura pública (semilleros, proyectos, eventos, publicaciones, ranking) |

---

## 4. FLUJOS PRINCIPALES

### 4.1 Flujo de Registro y Validación de Cuenta
1. Usuario solicita registro (nombre, correo, programa, documento)
2. Cuenta en estado "pendiente"
3. Administrador revisa solicitud
4. Si aprueba → estado "aprobada", puede hacer login
5. Si rechaza → estado "rechazada", no puede acceder

### 4.2 Flujo de Vinculación a Semillero
1. Estudiante explora semilleros
2. Solicita vinculación
3. Estado de vinculación: "solicitada"
4. Docente líder revisa
5. Si aprueba → estado "aprobada", estudiante es integrante
6. Si rechaza → estado "rechazada"
7. Puede retirarse posteriormente → estado "retirada"

### 4.3 Flujo de Publicación
1. Usuario crea publicación (título, contenido, categoría, evidencias)
2. Publicación aparece en feed
3. Otros usuarios pueden:
   - Reaccionar (UNIQUE usuario+publicación+tipo)
   - Comentar
   - Compartir
4. Sistema genera notificaciones

### 4.4 Flujo de Logro y XP
1. Usuario envía logro (tipo, título, evidencia)
2. Estado: "enviado"
3. Administrador valida
4. Si aprueba:
   - Estado cambia a "aprobado"
   - Sistema inserta movimiento XP (inmutable)
   - Recalcula XP total
   - Si supera umbral → sube de nivel/estrellas
   - Otorga insignias según reglas
   - Genera notificación
5. Si rechaza → estado "rechazado"

### 4.5 Flujo de Ranking
1. Cada semillero tiene XP total (suma de XP de integrantes)
2. Vista v_ranking_semilleros ordena por XP
3. Vista v_ranking_investigadores ordena por XP individual
4. Ranking se actualiza automáticamente con cada movimiento XP

---

## 5. REQUERIMIENTOS FUNCIONALES (RF)

### RF01 - Gestión de Usuarios
- RF01.1: Registro de cuenta institucional con validación administrativa
- RF01.2: Login con autenticación JWT
- RF01.3: Perfil de usuario con hoja de vida investigativa
- RF01.4: Asignación de roles (estudiante, docente, admin, visitante)
- RF01.5: Estados de cuenta (pendiente, aprobada, rechazada, suspendida)

### RF02 - Gestión de Investigación
- RF02.1: Gestión de semilleros por docente líder
- RF02.2: Líneas de investigación
- RF02.3: Vinculación de estudiantes a semilleros con aprobación
- RF02.4: Registro de proyectos y avances
- RF02.5: Registro de productos (artículos, ponencias, patentes, software)

### RF03 - Eventos y Convocatorias
- RF03.1: Consulta de eventos académicos
- RF03.2: Registro de participación en eventos
- RF03.3: Publicación de convocatorias
- RF03.4: Postulación a convocatorias
- RF03.5: Validación administrativa de convocatorias

### RF04 - Comunidad
- RF04.1: Creación de publicaciones con categorías y evidencias
- RF04.2: Comentarios en publicaciones
- RF04.3: Reacciones (UNIQUE usuario+publicación+tipo)
- RF04.4: Compartir publicaciones
- RF04.5: Seguimiento (follow) entre usuarios/semilleros
- RF04.6: Notificaciones de interacción

### RF05 - Gamificación
- RF05.1: Envío de logros con evidencia
- RF05.2: Validación de logros por administrador
- RF05.3: Asignación de XP al aprobar logro
- RF05.4: Niveles con umbrales de XP y estrellas 1-5
- RF05.5: Otorgamiento de insignias según reglas
- RF05.6: Ranking de semilleros e investigadores
- RF05.7: Historial inmutable de movimientos XP

### RF06 - Analítica
- RF06.1: Dashboard con KPIs
- RF06.2: Vista de ranking de semilleros
- RF06.3: Vista de ranking de investigadores
- RF06.4: Vista de XP por usuario
- RF06.5: Vista de impacto de publicaciones
- RF06.6: Vista de indicadores por facultad/programa
- RF06.7: Vista de hoja de vida investigativa

---

## 6. REQUERIMIENTOS NO FUNCIONALES (RNF)

### RNF01 - Seguridad
- RNF01.1: Autenticación JWT con tokens expirables
- RNF01.2: Control de acceso por rol
- RNF01.3: Hash de contraseñas con bcrypt
- RNF01.4: Permisos mínimos en BD
- RNF01.5: Validación de entrada anti SQL injection

### RNF02 - Almacenamiento
- RNF02.1: Almacenamiento de evidencias en volumen Docker
- RNF02.2: Metadatos de archivos en BD (nombre, tipo MIME, ruta, tamaño)
- RNF02.3: Volumen persistente para PostgreSQL

### RNF03 - Usabilidad
- RNF03.1: Dashboard intuitivo por rol
- RNF03.2: Navegación fluida entre módulos
- RNF03.3: Feedback visual en acciones (toasts, animaciones)
- RNF03.4: Diseño responsive (móvil/tablet/escritorio)

### RNF04 - Mantenibilidad
- RNF04.1: Arquitectura modular (BD, API, frontend separados)
- RNF04.2: Código legible y documentado
- RNF04.3: Lógica de negocio en BD (funciones, triggers)
- RNF04.4: API REST como puente delgado

### RNF05 - Reproducibilidad
- RNF05.1: Docker + Docker Compose
- RNF05.2: Entorno reproducible con un comando
- RNF05.3: Scripts de inicialización de BD
- RNF05.4: Variables de entorno sin secretos en repo

---

## 7. PALETA Y TIPOGRAFÍA (DEL PROTOTIPO)

### Colores
- Tinta principal: `#16213E` (var(--ink))
- Tinta suave: `#57638A` (var(--ink-soft))
- Papel: `#F3F5F8` (var(--paper))
- Superficie: `#FFFFFF` (var(--surface))
- Borde: `#E2E6ED` (var(--border))
- Acento (dorado): `#E3A008` (var(--accent))
- Acento ink: `#8A6100` (var(--accent-ink))
- Acento soft: `#FBEEC7` (var(--accent-soft))
- Teal: `#0F8B8D` (var(--teal))
- Rose: `#C23B70` (var(--rose))
- Green: `#2F8F5B` (var(--green))
- Red: `#C0392B` (var(--red))
- Violet: `#6C4FC2` (var(--violet))

### Tipografías
- Títulos: **Fraunces** (serif)
- Cuerpo: **Inter** (sans-serif)
- Datos/XP: **IBM Plex Mono** (monospace)

### Componentes del prototipo
- Avatar circular con iniciales
- Chips/tags con colores por estado
- Barra de progreso animada
- Badge hexagonal para nivel
- Estrellas SVG
- Cards con sombra
- Toasts de notificación
- Modal con overlay
- Tablas ordenables
- Iconos SVG (sprite)

---

## 8. TECNOLOGÍAS OBLIGATORIAS

### Frontend
- HTML5
- CSS3 (con variables CSS, organización base/components/pages)
- JavaScript vanilla (ES modules, fetch, sin frameworks)
- Tipografías de Google Fonts

### Backend
- Node.js 20
- Express
- Driver pg de PostgreSQL (sin ORM)
- bcrypt (hash de contraseñas)
- jsonwebtoken (JWT)
- multer (subida de archivos)

### Base de datos
- PostgreSQL 16
- Extensiones: pgcrypto, citext
- Lógica de negocio en BD (funciones, triggers, vistas)

### Infraestructura
- Docker
- Docker Compose
- nginx (sirve frontend y proxy a API)
- Adminer (inspección de BD)

---

## 9. ESTRUCTURA DEL PROYECTO

```
riul/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── database/
│   ├── init/
│   │   ├── 01_extensions_types.sql
│   │   ├── 02_schema.sql
│   │   ├── 03_functions_triggers.sql
│   │   ├── 04_views.sql
│   │   ├── 05_roles_security.sql
│   │   └── 06_seed.sql
│   ├── tests/
│   │   └── verify.sql
│   ├── ER_diagram.md
│   ├── diccionario_de_datos.md
│   └── README_db.md
├── api/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── config/
│       ├── db/
│       ├── middleware/
│       ├── routes/
│       └── controllers/
├── web/
│   ├── Dockerfile
│   ├── nginx/
│   │   └── default.conf
│   └── public/
│       ├── index.html
│       ├── pages/
│       ├── assets/
│       │   ├── css/
│       │   ├── js/
│       │   ├── img/
│       │   └── fonts/
└── docs/
    ├── entrada/
    │   ├── prototipo/
    │   ├── Descripcion_del_proyecto_RIUL.docx
    │   └── RIUL WORKFLOW.pdf
    ├── trazabilidad.md
    └── arquitectura.md
```

---

## 10. CRITERIOS DE ACEPTACIÓN

- [ ] `docker compose up --build` levanta 4 servicios (db, api, web, adminer) en estado healthy
- [ ] BD se crea automáticamente con tablas, funciones, triggers, vistas, roles y seed
- [ ] `database/tests/verify.sql` demuestra restricciones, triggers y vistas
- [ ] Modelo en 3FN, todas las FK/PK/índices definidos
- [ ] ER Mermaid renderiza correctamente
- [ ] Diccionario de datos cubre 100% de tablas
- [ ] Flujo completo de punta a punta funciona (registro → validación → login → vinculación → publicación → logro → XP)
- [ ] Cada módulo del prototipo tiene página, endpoints y tablas
- [ ] Matriz de trazabilidad completa
- [ ] README con requisitos, comandos, URLs, credenciales de demo

---

Este inventario servirá como base para:
1. Diseñar el esquema de base de datos
2. Implementar los endpoints de la API
3. Construir las páginas del frontend
4. Configurar Docker
5. Crear la matriz de trazabilidad
