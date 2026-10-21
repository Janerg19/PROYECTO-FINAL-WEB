# RIUL — Prototipo funcional

Prototipo interactivo (front-end únicamente, sin backend) de la Red de Investigación
Universidad Libre. Sirve para validar flujos de navegación y componentes de UI antes
de pasar a desarrollo real.

## Estructura del proyecto

```
riul-prototype/
├── index.html        # Estructura de todas las pantallas (login, dashboard, perfil, etc.)
├── css/
│   └── styles.css    # Tokens de diseño (colores, tipografía) y estilos de componentes
├── js/
│   └── app.js         # Estado en memoria + lógica de interacción (sin backend real)
└── assets/            # Carpeta libre para imágenes/logos que quieras agregar
```

## Cómo verlo en VS Code

1. Descomprime esta carpeta y ábrela en VS Code (`Archivo > Abrir carpeta...`).
2. Instala la extensión **Live Server** (Ritwick Dey) si no la tienes.
3. Clic derecho sobre `index.html` → **"Open with Live Server"**.
   - También puedes abrir `index.html` directamente con doble clic en el explorador
     de archivos del sistema operativo; funciona igual, ya que no depende de un servidor.

## Qué es funcional en este prototipo

- **Login**: elegir un rol de demo e iniciar sesión entra al panel real.
- **Registro**: formulario alterno dentro de la misma tarjeta de login.
- **Selector de rol** (barra superior): cambia el menú lateral y los permisos en vivo
  (Estudiante, Docente líder, Administrador, Visitante).
- **Publicaciones**: modal "Crear publicación" agrega tarjetas reales al feed.
- **Perfil**: "Registrar nuevo logro" agrega ítems a la lista de pendientes.
- **Gamificación**: botón "Simular actividad" anima la barra de XP y sube de nivel.
- **Panel admin**: "Aprobar" / "Rechazar" quita filas de las tablas de validación.
- **Ranking**: clic en encabezados de columna para ordenar la tabla.

Todo el estado vive en memoria (`js/app.js`, objeto `state`) y se reinicia al recargar
la página — no hay conexión a una base de datos ni a un servidor.

## Próximos pasos sugeridos

- Conectar `submitPost()`, `submitLogro()` y `resolveRow()` a endpoints reales (REST o
  GraphQL) en lugar de mutar el objeto `state` en memoria.
- Añadir autenticación real (JWT / sesión institucional) en vez del selector de rol de
  la demo.
- Extraer los componentes repetidos (tarjeta de publicación, chip, badge de nivel) a
  componentes de un framework (React/Vue) si el proyecto crece.

## Paleta y tipografía

- Tinta principal: `#16213E` — dorado de acento (XP / niveles): `#E3A008`
- Tipografías: **Fraunces** (títulos), **Inter** (cuerpo), **IBM Plex Mono** (datos/XP),
  cargadas desde Google Fonts en `index.html`.
