# Base de Datos - RIUL

Documentación de la base de datos de la Red de Investigación Universidad Libre.

## Índice

- [Decisiones de Diseño](#decisiones-de-diseño)
- [Normalización](#normalización)
- [Conexión a la Base de Datos](#conexión-a-la-base-de-datos)
- [Reinicio de la Base de Datos](#reinicio-de-la-base-de-datos)
- [Scripts de Inicialización](#scripts-de-inicialización)
- [Seguridad](#seguridad)
- [Pruebas](#pruebas)

---

## Decisiones de Diseño

### 1. Elección de PK (IDENTITY vs UUID)

**Decisión**: Usamos `SERIAL` (IDENTITY) para todas las PKs.

**Justificación**:
- Simplicidad: `SERIAL` es más simple y no requiere funciones de generación
- Performance: Los enteros son más rápidos para joins y comparaciones
- Suficiente para el proyecto: No se espera escalabilidad masiva que requiera UUIDs
- Compatibilidad: Compatible con ORMs y herramientas de visualización

### 2. Timestamps

**Decisión**: Todas las tablas tienen `creado_en` y las tablas modificables tienen `actualizado_en`.

**Justificación**:
- `creado_en`: Para trazabilidad y auditoría
- `actualizado_en`: Para saber cuándo se modificó un registro por última vez
- Ambos se actualizan automáticamente con triggers

### 3. Borrado Lógico

**Decisión**: Las tablas principales (`usuario`, `semillero`, `proyecto`, `publicacion`, `comentario`) tienen `eliminado_en` para borrado lógico.

**Justificación**:
- Preservar historial de investigaciones y publicaciones
- Permitir recuperación de datos eliminados por error
- Mantener integridad referencial (evitar "orphan records")
- Las tablas de relación (N:M) usan `ON DELETE CASCADE` real

### 4. XP Total y Nivel

**Decisión**: `usuario.xp_total` y `usuario.nivel_id` se mantienen por triggers.

**Justificación**:
- Performance: Evitar cálculos repetitivos de SUM() en cada consulta
- Facilitar ranking y consultas frecuentes
- Se actualizan automáticamente al insertar en `movimiento_xp`
- Alternativa: Vista materializada refrescada periódicamente

### 5. Polimorfismo de Evidencias

**Decisión**: `evidencia` es una tabla central con tablas puente (`publicacion_evidencia`, `logro_evidencia`).

**Justificación**:
- Reutilización: La misma tabla de evidencias para publicaciones y logros
- Normalización: Evitar duplicar metadatos de archivos
- Flexibilidad: Fácil agregar nuevas entidades que usen evidencias
- Alternativa rechazada: Columna polimórfica (evidencia_tipo, evidencia_id) que rompe integridad referencial

### 6. Movimiento XP Inmutable

**Decisión**: `movimiento_xp` es inmutable (trigger impide modificaciones/eliminaciones).

**Justificación**:
- Integridad: El historial de XP no debe alterarse
- Auditoría: Permite rastrear todos los movimientos de XP
- Seguridad: Evita manipulación de puntos por usuarios con acceso directo

### 7. Índices

**Decisión**: Índices en todas las FK y columnas de búsqueda frecuentes.

**Justificación**:
- Performance: Mejora tiempos de consulta en joins y filtros
- Índices parciales: Para consultas específicas (ej. `WHERE leida = FALSE`)
- Índices compuestos: Para patrones de consulta comunes

### 8. Tipos ENUM

**Decisión**: Usar ENUMs para estados y categorías fijas.

**Justificación**:
- Type safety: El motor de BD valida los valores
- Performance: Más eficiente que strings en comparaciones
- Documentación: Los valores posibles están definidos en el esquema
- Legibilidad: Código más legible que enteros mágicos

---

## Normalización

El esquema está normalizado hasta **Tercera Forma Normal (3FN)**:

### 1FN (Primera Forma Normal)
- Todos los atributos son atómicos (no hay arrays repetidos)
- Existe una PK única por tabla
- No hay filas duplicadas

**Excepción justificada**: `perfil_investigador.intereses` es un array de strings. Esto se justifica porque:
- Los intereses son una lista de categorías, no datos relacionales
- Facilita búsquedas con `ANY()` y `ALL()`
- Evita una tabla N:M adicional con poca ganancia semántica

### 2FN (Segunda Forma Normal)
- Todos los atributos no clave dependen completamente de la PK
- No hay dependencias parciales

**Ejemplo**: `semillero_integrante` tiene PK compuesta `(semillero_id, usuario_id)`. Todos los atributos (`rol`, `estado`, `fecha_solicitud`) dependen de la PK completa, no de una sola parte.

### 3FN (Tercera Forma Normal)
- No hay dependencias transitivas
- Los atributos no clave no dependen de otros atributos no clave

**Excepción justificada**: `usuario.xp_total` y `usuario.nivel_id` dependen de la suma de `movimiento_xp`. Se mantienen por triggers por performance, pero el valor "verdadero" está en `movimiento_xp`.

---

## Conexión a la Base de Datos

### Desde Docker (recomendado)

```bash
# Entrar al contenedor de PostgreSQL
docker exec -it riul-db psql -U riul_app -d riul

# O usando psql desde el host
psql -h localhost -p 5432 -U riul_app -d riul
```

### Variables de Entorno

Las credenciales se configuran en `.env`:

```env
DB_HOST=riul-db
DB_PORT=5432
DB_NAME=riul
DB_USER=riul_app
DB_PASSWORD=cambiar_esto_en_produccion
```

### Desde Node.js

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});
```

### Desde Adminer

- URL: http://localhost:8081
- Servidor: riul-db
- Usuario: riul_app
- Contraseña: (configurada en .env)
- Base de datos: riul

---

## Reinicio de la Base de Datos

### Reinicio Completo (borra todo)

```bash
# Detener y eliminar volúmenes
docker compose down -v

# Reconstruir y levantar
docker compose up --build
```

**Advertencia**: Esto borra todos los datos, incluyendo los datos semilla.

### Reinicio Solo de Datos (conserva esquema)

```bash
# Entrar al contenedor
docker exec -it riul-db psql -U riul_app -d riul

# Ejecutar script de seed
\i /docker-entrypoint-initdb.d/06_seed.sql
```

### Backup

```bash
# Backup desde el contenedor
docker exec riul-db pg_dump -U riul_app riul > backup.sql

# Backup desde el host
pg_dump -h localhost -U riul_app riul > backup.sql
```

### Restauración

```bash
# Restaurar en el contenedor
docker exec -i riul-db psql -U riul_app riul < backup.sql

# Restaurar desde el host
psql -h localhost -U riul_app riul < backup.sql
```

---

## Scripts de Inicialización

Los scripts en `database/init/` se ejecutan automáticamente al crear el contenedor de PostgreSQL, en orden numérico:

### 01_extensions_types.sql
- Crea extensiones (`pgcrypto`, `citext`)
- Crea ENUMs (estados, tipos, roles)
- Crea tablas catálogo (rol, facultad, programa, tipo_actividad_xp, nivel, insignia, categoria_publicacion)

### 02_schema.sql
- Crea todas las tablas principales
- Define PK, FK, UNIQUE, CHECK
- Crea índices
- Añade columnas de gamificación a `usuario` (xp_total, nivel_id)

### 03_functions_triggers.sql
- Crea trigger genérico `actualizar_timestamp()`
- Crea funciones de gamificación (`actualizar_xp_usuario`, `insertar_movimiento_xp`, `otorgar_insignias_usuario`)
- Crea triggers de lógica de negocio (aprobación de logro, vinculación, publicaciones, etc.)
- Crea triggers de seguridad (movimiento_xp inmutable, doble vinculación, doble reacción)

### 04_views.sql
- Crea vistas de analítica (ranking, XP por usuario, impacto de publicaciones, indicadores institucionales)
- Crea vistas de administración (logros pendientes, cuentas pendientes)
- Crea vista de hoja de vida investigativa

### 05_roles_security.sql
- Crea roles de BD (`riul_app`, `riul_readonly`)
- Otorga permisos mínimos a `riul_app`
- Otorga permisos de solo lectura a `riul_readonly`
- Configura `ALTER DEFAULT PRIVILEGES` para objetos futuros

### 06_seed.sql
- Inserta datos semilla realistas
- Crea usuarios, facultades, programas, semilleros, proyectos, eventos, convocatorias
- Crea publicaciones, comentarios, reacciones, compartidos
- Crea logros, movimientos XP, insignias
- Crea notificaciones

---

## Seguridad

### Roles de Base de Datos

#### riul_app (Rol de Aplicación)
- Permisos: SELECT, INSERT, UPDATE, DELETE en todas las tablas
- Permisos: USAGE, SELECT en todas las secuencias
- Permisos: EXECUTE en todas las funciones
- Permisos: SELECT en todas las vistas
- **NO** tiene SUPERUSER, CREATEDB, CREATEROLE

#### riul_readonly (Rol de Analítica)
- Permisos: SELECT en todas las tablas y vistas
- Permisos: USAGE, SELECT en todas las secuencias
- Permisos: EXECUTE en funciones de solo lectura
- **NO** puede INSERT, UPDATE, DELETE

### Seguridad en la Aplicación

- **Contraseñas**: Se hashean con bcrypt en la aplicación, no en BD
- **JWT**: Tokens expirables para autenticación
- **Validación de entrada**: Consultas parametrizadas (anti SQL injection)
- **Control de acceso por rol**: La API valida permisos antes de ejecutar consultas

### Reglas de Negocio en BD

- Solo administradores pueden validar logros (validado en trigger)
- Movimientos XP son inmutables (trigger impide modificaciones)
- No se puede vincular dos veces al mismo semillero (trigger impide duplicados)
- No se puede reaccionar dos veces con el mismo tipo (trigger impide duplicados)

---

## Pruebas

### Ejecutar Script de Verificación

```bash
# Desde el contenedor
docker exec -it riul-db psql -U riul_app -d riul -f /docker-entrypoint-initdb.d/../tests/verify.sql

# Desde el host
psql -h localhost -U riul_app -d riul -f database/tests/verify.sql
```

### Qué Verifica el Script

1. **Restricciones de integridad**: PK, FK, UNIQUE, CHECK
2. **Triggers de lógica de negocio**: actualizado_en, movimiento_xp inmutable
3. **Funciones de gamificación**: insertar_movimiento_xp, actualizar_xp_usuario
4. **Funciones de vinculación**: solicitar_vinculacion, resolver_vinculacion
5. **Vistas de analítica**: Todas las vistas retornan datos correctamente
6. **Flujo completo de logro**: Aprobación → XP → Nivel → Insignias → Notificación

### Resultado Esperado

Todas las pruebas deben mostrar `✓` (éxito). Si hay `✗`, revise los errores en los logs.

---

## Diagrama ER

El diagrama entidad-relación completo está en `ER_diagram.md` en formato Mermaid.

Para visualizarlo:

1. Copie el código Mermaid
2. Péguelo en [Mermaid Live Editor](https://mermaid.live/)
3. O use una extensión de VS Code que soporte Mermaid

---

## Diccionario de Datos

El diccionario de datos completo está en `diccionario_de_datos.md`.

Describe cada tabla, sus atributos, tipos, restricciones y descripciones.

---

## Contacto

Para preguntas sobre la base de datos, consulte:
- Documentación del proyecto: `README.md`
- Matriz de trazabilidad: `docs/trazabilidad.md`
- Arquitectura: `docs/arquitectura.md`
