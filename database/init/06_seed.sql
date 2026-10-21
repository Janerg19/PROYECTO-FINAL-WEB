-- ==========================================
-- 06_seed.sql
-- Datos semilla realistas para demostración
-- ==========================================

-- NOTA: Las contraseñas están hasheadas con bcrypt para "Password123!"
-- Usuario admin: admin@unilibre.edu.co / Password123!
-- Usuario docente: docente1@unilibre.edu.co / Password123!
-- Usuario estudiante: estudiante1@unilibre.edu.co / Password123!

-- ==========================================
-- ROLES DEL SISTEMA
-- ==========================================

INSERT INTO rol (nombre, descripcion) VALUES
('estudiante', 'Estudiante investigador'),
('docente', 'Docente líder de semillero'),
('administrador', 'Administrador del sistema'),
('visitante', 'Visitante con solo lectura');

-- ==========================================
-- FACULTADES
-- ==========================================

INSERT INTO facultad (nombre, codigo) VALUES
('Facultad de Ingeniería', 'ING'),
('Facultad de Ciencias', 'CIE'),
('Facultad de Derecho', 'DER');

-- ==========================================
-- PROGRAMAS
-- ==========================================

INSERT INTO programa (facultad_id, nombre, codigo, tipo) VALUES
-- Ingeniería
(1, 'Ingeniería de Sistemas', 'IS', 'pregrado'),
(1, 'Ingeniería Electrónica', 'IE', 'pregrado'),
(1, 'Ingeniería Industrial', 'II', 'pregrado'),
-- Ciencias
(2, 'Biología', 'BIO', 'pregrado'),
(2, 'Matemáticas', 'MAT', 'pregrado'),
-- Derecho
(3, 'Derecho', 'DER', 'pregrado');

-- ==========================================
-- TIPOS DE ACTIVIDAD CON XP
-- ==========================================

INSERT INTO tipo_actividad_xp (tipo, xp_base, descripcion) VALUES
('registro_usuario', 50, 'Registro de cuenta validada'),
('vinculacion_semillero', 100, 'Vinculación aprobada a semillero'),
('publicacion', 80, 'Publicación creada'),
('comentario', 20, 'Comentario en publicación'),
('reaccion', 10, 'Reacción a publicación'),
('proyecto_registrado', 150, 'Proyecto registrado'),
('producto_registrado', 200, 'Producto registrado (artículo, ponencia, etc.)'),
('evento_participacion', 40, 'Participación en evento'),
('logro_validado', 300, 'Logro validado por administrador');

-- ==========================================
-- NIVELES DE GAMIFICACIÓN
-- ==========================================

INSERT INTO nivel (numero, umbral_xp, estrellas, descripcion) VALUES
(1, 1, 1, 'Investigador novato'),
(2, 500, 2, 'Investigador aprendiz'),
(3, 1000, 3, 'Investigador competente'),
(4, 2000, 4, 'Investigador experto'),
(5, 4000, 5, 'Investigador maestro');

-- ==========================================
-- INSIGNIAS
-- ==========================================

INSERT INTO insignia (nombre, descripcion, criterio, icono, color) VALUES
('Primeros pasos', 'Completó el registro inicial', 'registro_usuario', 'i-user', '#6C4FC2'),
('Nivel 3 alcanzado', 'Alcanzó el nivel 3 de investigación', 'nivel >= 3', 'i-star', '#E3A008'),
('1000 XP', 'Acumuló 1000 XP', 'xp_total >= 1000', 'i-trophy', '#0F8B8D'),
('5 logros validados', 'Tiene 5 logros validados', 'num_logros_aprobados >= 5', 'i-shield', '#C23B70'),
('10 publicaciones', 'Realizó 10 publicaciones', 'num_publicaciones >= 10', 'i-doc', '#2F8F5B'),
('Líder de semillero', 'Es líder de un semillero activo', 'lider_semillero', 'i-flask', '#16213E');

-- ==========================================
-- CATEGORÍAS DE PUBLICACIÓN
-- ==========================================

INSERT INTO categoria_publicacion (nombre, descripcion, color) VALUES
('Logro', 'Publicación de logros investigativos', '#E3A008'),
('Proyecto', 'Avances de proyectos', '#0F8B8D'),
('Evento', 'Participación en eventos', '#C23B70'),
('General', 'Publicaciones generales', '#6C4FC2');

-- ==========================================
-- USUARIOS
-- ==========================================

-- Contraseña hasheada con bcrypt para "Password123!"
-- Hash generado con bcrypt (cost factor 10)

INSERT INTO usuario (rol_id, nombres, apellidos, email, password_hash, estado, xp_total, nivel_id) VALUES
-- Administrador
(4, 'Alfonso', 'Lopez', 'admin@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 2500, 4),

-- Docentes líderes
(3, 'Andrea', 'Molina', 'docente1@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 1800, 3),
(3, 'Roberto', 'Sánchez', 'docente2@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 1500, 3),
(3, 'María', 'García', 'docente3@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 1200, 2),

-- Estudiantes
(1, 'Juliana', 'Díaz', 'estudiante1@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 1240, 3),
(1, 'Camilo', 'Rojas', 'estudiante2@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 980, 2),
(1, 'Laura', 'Gómez', 'estudiante3@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 850, 2),
(1, 'David', 'Ruiz', 'estudiante4@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 720, 2),
(1, 'Paula', 'León', 'estudiante5@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 650, 2),
(1, 'Iván', 'Cárdenas', 'estudiante6@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'aprobada', 580, 1),

-- Cuentas pendientes
(1, 'Ana', 'Martínez', 'ana.martinez@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'pendiente', 0, 1),
(1, 'Juan', 'Torres', 'juan.torres@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'pendiente', 0, 1),

-- Cuenta rechazada
(1, 'Pedro', 'Vargas', 'pedro.vargas@unilibre.edu.co', '$2b$10$rTBA4pWTVYnlMJYmH6kP..sJ1UAVmQ.frNS4DgrtX21lMRwVTxWVe', 'rechazada', 0, 1);

-- Actualizar validador para el admin
UPDATE usuario SET validado_por = 1, fecha_validacion = CURRENT_TIMESTAMP WHERE id = 1;

-- ==========================================
-- PERFILES INVESTIGATIVOS
-- ==========================================

INSERT INTO perfil_investigador (usuario_id, biografia, intereses, orcid) VALUES
(5, 'Estudiante de Ingeniería de Sistemas con interés en IA y ciencia de datos.', ARRAY['Inteligencia Artificial', 'Ciencia de Datos', 'Machine Learning'], '0000-0001-2345-6789'),
(6, 'Estudiante de Ingeniería Electrónica enfocado en IoT y sistemas embebidos.', ARRAY['IoT', 'Sistemas Embebidos', 'Electrónica'], NULL),
(7, 'Estudiante de Biología interesada en bioinformática y genómica.', ARRAY['Bioinformática', 'Genómica', 'Biología Computacional'], '0000-0002-3456-7890'),
(8, 'Estudiante de Matemáticas con interés en modelado matemático.', ARRAY['Modelado Matemático', 'Estadística', 'Optimización'], NULL);

-- ==========================================
-- USUARIO-PROGRAMA
-- ==========================================

INSERT INTO usuario_programa (usuario_id, programa_id, fecha_inicio, actual) VALUES
(1, 1, '2020-01-15', TRUE), -- Admin - Ingeniería de Sistemas
(2, 1, '2018-03-01', TRUE), -- Docente 1 - Ingeniería de Sistemas
(3, 2, '2017-07-15', TRUE), -- Docente 2 - Ingeniería Electrónica
(4, 4, '2019-02-20', TRUE), -- Docente 3 - Biología
(5, 1, '2023-01-10', TRUE), -- Estudiante 1 - Ingeniería de Sistemas
(6, 2, '2023-01-10', TRUE), -- Estudiante 2 - Ingeniería Electrónica
(7, 4, '2023-01-10', TRUE), -- Estudiante 3 - Biología
(8, 5, '2023-01-10', TRUE), -- Estudiante 4 - Matemáticas
(9, 1, '2023-01-10', TRUE), -- Estudiante 5 - Ingeniería de Sistemas
(10, 1, '2023-01-10', TRUE), -- Estudiante 6 - Ingeniería de Sistemas
(11, 1, '2024-01-15', TRUE), -- Pendiente 1
(12, 1, '2024-01-20', TRUE); -- Pendiente 2

-- ==========================================
-- LÍNEAS DE INVESTIGACIÓN
-- ==========================================

INSERT INTO linea_investigacion (nombre, descripcion) VALUES
('Inteligencia Artificial', 'Investigación en IA, machine learning y deep learning'),
('Bioinformática', 'Aplicación de computación a problemas biológicos'),
('IoT y Sistemas Embebidos', 'Internet de las cosas y sistemas embebidos'),
('Modelado Matemático', 'Modelado matemático de fenómenos naturales y sociales'),
('Ingeniería de Software', 'Metodologías, procesos y herramientas de software');

-- ==========================================
-- SEMILLEROS
-- ==========================================

INSERT INTO semillero (nombre, descripcion, facultad_id, programa_id, lider_id, fecha_creacion) VALUES
('RIUL-Dev', 'Semillero de investigación en desarrollo de software y trazabilidad académica', 1, 1, 2, '2023-01-15'),
('BioUL', 'Semillero de bioinformática y genómica computacional', 2, 4, 4, '2022-06-20'),
('IoT Lab', 'Laboratorio de investigación en IoT y sistemas embebidos', 1, 2, 3, '2023-03-10'),
('MathModel', 'Modelado matemático aplicado a problemas reales', 2, 5, 3, '2022-09-15'),
('DataMind', 'Ciencia de datos y analítica avanzada', 1, 1, 2, '2023-05-20');

-- ==========================================
-- SEMILLERO-LÍNEA
-- ==========================================

INSERT INTO semillero_linea (semillero_id, linea_id) VALUES
(1, 5), -- RIUL-Dev - Ingeniería de Software
(1, 1), -- RIUL-Dev - IA
(2, 2), -- BioUL - Bioinformática
(3, 3), -- IoT Lab - IoT
(4, 4), -- MathModel - Modelado Matemático
(5, 1), -- DataMind - IA
(5, 4); -- DataMind - Modelado Matemático

-- ==========================================
-- INTEGRANTES DE SEMILLERO
-- ==========================================

-- RIUL-Dev (id=1)
INSERT INTO semillero_integrante (semillero_id, usuario_id, rol, estado, fecha_solicitud, fecha_resolucion, revisado_por) VALUES
(1, 2, 'lider', 'aprobada', '2023-01-15', '2023-01-15', 1), -- Docente líder
(1, 5, 'estudiante', 'aprobada', '2023-02-01', '2023-02-02', 2), -- Juliana
(1, 9, 'estudiante', 'aprobada', '2023-03-01', '2023-03-02', 2), -- Paula
(1, 10, 'estudiante', 'solicitada', '2024-01-10', NULL, NULL), -- Iván (pendiente)
(1, 6, 'estudiante', 'retirada', '2023-04-01', '2023-06-01', 2); -- Camilo (retirado)

-- BioUL (id=2)
INSERT INTO semillero_integrante (semillero_id, usuario_id, rol, estado, fecha_solicitud, fecha_resolucion, revisado_por) VALUES
(2, 4, 'lider', 'aprobada', '2022-06-20', '2022-06-20', 1), -- Docente líder
(2, 7, 'estudiante', 'aprobada', '2022-07-01', '2022-07-02', 4), -- Laura
(2, 8, 'estudiante', 'aprobada', '2022-08-01', '2022-08-02', 4); -- David

-- IoT Lab (id=3)
INSERT INTO semillero_integrante (semillero_id, usuario_id, rol, estado, fecha_solicitud, fecha_resolucion, revisado_por) VALUES
(3, 3, 'lider', 'aprobada', '2023-03-10', '2023-03-10', 1), -- Docente líder
(3, 6, 'estudiante', 'aprobada', '2023-04-01', '2023-04-02', 3); -- Camilo

-- DataMind (id=5)
INSERT INTO semillero_integrante (semillero_id, usuario_id, rol, estado, fecha_solicitud, fecha_resolucion, revisado_por) VALUES
(5, 2, 'lider', 'aprobada', '2023-05-20', '2023-05-20', 1), -- Docente líder
(5, 5, 'estudiante', 'aprobada', '2023-06-01', '2023-06-02', 2); -- Juliana

-- ==========================================
-- PROYECTOS
-- ==========================================

INSERT INTO proyecto (titulo, descripcion, semillero_id, estado, fecha_inicio, fecha_fin) VALUES
('Plataforma de trazabilidad académica', 'Desarrollo de plataforma para seguimiento de semilleros y proyectos.', 1, 'en_curso', '2023-02-01', '2024-12-31'),
('Predicción de deserción estudiantil', 'Modelo de machine learning para predecir deserción estudiantil.', 5, 'en_curso', '2023-06-01', '2024-06-30'),
('Análisis genómico de especies nativas', 'Secuenciación y análisis de genomas de especies colombianas.', 2, 'en_curso', '2022-08-01', '2024-12-31'),
('Sistema de monitoreo IoT para laboratorios', 'Desarrollo de sistema IoT para monitoreo de condiciones ambientales.', 3, 'formulacion', '2023-05-01', '2024-05-31'),
('Optimización de rutas logísticas', 'Modelado matemático para optimización de rutas de transporte.', 4, 'finalizado', '2022-10-01', '2023-09-30'),
('Asistente virtual para investigación', 'Desarrollo de asistente virtual con IA para investigadores.', 1, 'en_curso', '2023-08-01', '2024-08-31'),
('Dashboard de analítica institucional', 'Dashboard interactivo para visualización de indicadores.', 5, 'en_curso', '2023-09-01', '2024-03-31'),
('Sistema de gestión de evidencias', 'Sistema para gestión y almacenamiento de evidencias de investigación.', 1, 'formulacion', '2023-10-01', '2024-10-31');

-- ==========================================
-- INTEGRANTES DE PROYECTO
-- ==========================================

INSERT INTO proyecto_integrante (proyecto_id, usuario_id, rol) VALUES
(1, 2, 'investigador'), -- Plataforma de trazabilidad - Docente
(1, 5, 'investigador'), -- Juliana
(1, 9, 'investigador'), -- Paula
(2, 2, 'investigador'), -- Predicción deserción - Docente
(2, 5, 'investigador'), -- Juliana
(3, 4, 'investigador'), -- Análisis genómico - Docente
(3, 7, 'investigador'), -- Laura
(3, 8, 'investigador'), -- David
(4, 3, 'investigador'), -- IoT - Docente
(4, 6, 'investigador'); -- Camilo

-- ==========================================
-- AVANCES DE PROYECTO
-- ==========================================

INSERT INTO avance_proyecto (proyecto_id, titulo, descripcion, fecha_avance, creado_por) VALUES
(1, 'Diseño de esquema de base de datos', 'Se completó el diseño del esquema relacional para la plataforma.', '2023-03-15', 2),
(1, 'Implementación de API REST', 'Se implementaron los endpoints principales de la API.', '2023-05-20', 5),
(2, 'Recolección de datos históricos', 'Se recopilaron 5 años de datos estudiantiles para entrenamiento.', '2023-07-10', 2),
(2, 'Entrenamiento de modelo inicial', 'Se entrenó el primer modelo con accuracy del 78%.', '2023-09-15', 5),
(3, 'Secuenciación de primeras muestras', 'Se secuenciaron 50 muestras de especies nativas.', '2022-10-01', 4),
(3, 'Análisis preliminar de datos', 'Se realizó análisis de calidad de datos genómicos.', '2023-01-15', 7);

-- ==========================================
-- PRODUCTOS
-- ==========================================

INSERT INTO producto (proyecto_id, titulo, tipo, descripcion, fecha_publicacion, url, creado_por) VALUES
(1, 'Artículo: Trazabilidad académica con PostgreSQL', 'articulo', 'Artículo aceptado en revista indexada sobre diseño de BD.', '2023-06-15', 'https://revista-ejemplo.com/articulo-123', 5),
(1, 'Ponencia: Plataforma RIUL en congreso nacional', 'ponencia', 'Ponencia presentada en Congreso Nacional de Ingeniería de Software.', '2023-08-20', NULL, 2),
(2, 'Artículo: Predicción de deserción con ML', 'articulo', 'Artículo sobre modelo de predicción de deserción estudiantil.', '2023-10-10', 'https://revista-ejemplo.com/articulo-456', 5),
(3, 'Software: BioAnalyzer v1.0', 'software', 'Herramienta de análisis de secuencias genómicas.', '2023-05-01', 'https://github.com/bioul/bioanalyzer', 7),
(3, 'Artículo: Genoma de especie nativa', 'articulo', 'Publicación del genoma secuenciado de una especie nativa.', '2023-07-20', 'https://revista-ejemplo.com/articulo-789', 4),
(4, 'Patente: Sistema de monitoreo IoT', 'patente', 'Sistema patentado para monitoreo de laboratorios.', '2023-12-01', NULL, 3);

-- ==========================================
-- EVENTOS
-- ==========================================

INSERT INTO evento (titulo, descripcion, fecha_evento, hora, lugar, creado_por) VALUES
('Coloquio de semilleros 2026', 'Evento anual de presentación de resultados de semilleros.', '2026-10-20', '10:00', 'Auditorio principal', 1),
('Taller de escritura científica', 'Taller práctico sobre redacción de artículos científicos.', '2026-11-15', '14:00', 'Bloque B - Sala 301', 2),
('Feria de proyectos 2026', 'Exposición de proyectos de investigación de todos los semilleros.', '2026-12-10', '09:00', 'Plazoleta central', 1),
('Seminario de Inteligencia Artificial', 'Seminario sobre avances en IA y sus aplicaciones.', '2026-10-25', '16:00', 'Auditorio de Ingeniería', 2),
('Workshop de Bioinformática', 'Workshop sobre herramientas de análisis genómico.', '2026-11-05', '10:00', 'Laboratorio de Biología', 4),
('Hackathon de Datos', 'Competencia de análisis de datos en tiempo real.', '2026-12-05', '09:00', 'Sala de computación', 2);

-- ==========================================
-- PARTICIPACIÓN EN EVENTOS
-- ==========================================

INSERT INTO participacion_evento (evento_id, usuario_id, rol) VALUES
(1, 5, 'ponente'), -- Juliana - Coloquio
(1, 2, 'organizador'), -- Docente - Coloquio
(1, 7, 'asistente'), -- Laura - Coloquio
(2, 5, 'asistente'), -- Juliana - Taller
(2, 6, 'asistente'), -- Camilo - Taller
(3, 2, 'organizador'), -- Docente - Feria
(3, 5, 'asistente'), -- Juliana - Feria
(4, 5, 'asistente'), -- Juliana - Seminario IA
(5, 7, 'asistente'), -- Laura - Workshop
(5, 8, 'asistente'); -- David - Workshop

-- ==========================================
-- CONVOCATORIAS
-- ==========================================

INSERT INTO convocatoria (titulo, descripcion, estado, fecha_apertura, fecha_cierre, validado_por, fecha_validacion, creado_por) VALUES
('Semilleros de investigación aplicada 2026-II', 'Financiación para proyectos de investigación aplicada en curso.', 'publicada', '2026-09-01', '2026-10-31', 1, '2026-09-05', 1),
('Movilidad académica internacional', 'Apoyo para presentar resultados en congresos internacionales.', 'publicada', '2026-10-01', '2026-11-30', 1, '2026-10-05', 1),
('Publicación en revistas indexadas', 'Apoyo para costos de publicación en revistas indexadas.', 'publicada', '2026-09-15', '2026-12-15', 1, '2026-09-20', 1),
('Equipamiento de laboratorios', 'Financiación para equipamiento de laboratorios de investigación.', 'borrador', '2026-11-01', '2027-01-31', NULL, NULL, 1);

-- ==========================================
-- POSTULACIONES A CONVOCATORIAS
-- ==========================================

INSERT INTO postulacion_convocatoria (convocatoria_id, usuario_id, propuesta, estado, fecha_postulacion) VALUES
(1, 5, 'Proyecto: Plataforma de trazabilidad académica - fase 2', 'aprobada', '2026-09-10'),
(1, 7, 'Proyecto: Análisis genómico de especies nativas - fase 2', 'en_revision', '2026-09-15'),
(2, 5, 'Ponencia: Congreso Internacional de Ingeniería de Software', 'enviada', '2026-10-10'),
(2, 7, 'Ponencia: Congreso de Bioinformática', 'enviada', '2026-10-12'),
(3, 2, 'Artículo: Trazabilidad académica con PostgreSQL', 'aprobada', '2026-09-20');

-- ==========================================
-- PUBLICACIONES
-- ==========================================

INSERT INTO publicacion (categoria_id, usuario_id, semillero_id, titulo, contenido) VALUES
(1, 5, 1, 'Artículo aceptado en revista indexada', 'El artículo sobre trazabilidad académica fue aceptado para publicación en la revista de la facultad. Este es un hito importante para nuestro semillero.'),
(2, 5, 1, 'Avance del prototipo de dashboard', 'Compartimos capturas del dashboard institucional en su primera versión funcional. El prototipo permite visualizar indicadores de investigación en tiempo real.'),
(3, 5, NULL, 'Participación en coloquio nacional', 'Presentamos resultados preliminares del proyecto de bioinformática en el coloquio nacional de semilleros. Fue una excelente oportunidad de difusión.'),
(1, 7, 2, 'Secuenciación completada', 'Hemos completado la secuenciación de 50 muestras de especies nativas. Los resultados preliminares son muy prometedores.'),
(2, 2, 1, 'Nuevo proyecto de predicción de deserción', 'Iniciamos un nuevo proyecto para predecir deserción estudiantil usando machine learning. Estamos recopilando datos históricos.'),
(4, 6, 3, 'Bienvenidos al IoT Lab', 'El semillero IoT Lab ha iniciado actividades. Investigaremos sistemas de monitoreo IoT para laboratorios.'),
(1, 2, 1, 'Patente en proceso', 'Hemos presentado una solicitud de patente para nuestro sistema de monitoreo IoT. Esperamos noticias pronto.'),
(2, 8, 2, 'Modelo matemático optimizado', 'Mejoramos el algoritmo de optimización de rutas logísticas, reduciendo el tiempo de cómputo en un 40%.'),
(3, 5, NULL, 'Taller de escritura científica', 'Asistí al taller de escritura científica. Aprendí muchas técnicas para mejorar mis artículos.'),
(1, 9, 1, 'Primer logro validado', '¡Mi primer logro ha sido validado! Ya tengo 300 XP adicionales.'),
(4, 10, 1, 'Inscripción a semillero', 'Acabo de solicitar mi vinculación al semillero RIUL-Dev. Espero ser aprobado pronto.'),
(2, 4, 2, 'Publicación en Nature', 'Nuestro artículo sobre genoma de especie nativa fue aceptado en Nature. Un logro histórico para el semillero.'),
(1, 5, 5, 'Dashboard de analítica', 'Completamos el dashboard de analítica institucional. Ahora podemos visualizar indicadores por facultad y programa.'),
(3, 7, 2, 'Conferencia internacional', 'Viajaré a Europa para presentar nuestros resultados en una conferencia internacional de bioinformática.'),
(4, 2, 1, 'Convocatoria abierta', 'Se ha abierto una nueva convocatoria para financiación de proyectos. ¡No pierdan la oportunidad!');

-- ==========================================
-- EVIDENCIAS
-- ==========================================

INSERT INTO evidencia (nombre_archivo, tipo_mime, tamano_bytes, ruta) VALUES
('articulo_trazabilidad.pdf', 'application/pdf', 2457600, '/uploads/evidencias/articulo_trazabilidad.pdf'),
('dashboard_screenshot.png', 'image/png', 512000, '/uploads/evidencias/dashboard_screenshot.png'),
('coloquio_certificado.pdf', 'application/pdf', 153600, '/uploads/evidencias/coloquio_certificado.pdf'),
('secuenciacion_reporte.pdf', 'application/pdf', 3072000, '/uploads/evidencias/secuenciacion_reporte.pdf'),
('patente_documento.pdf', 'application/pdf', 5120000, '/uploads/evidencias/patente_documento.pdf'),
('logro_evidencia.pdf', 'application/pdf', 102400, '/uploads/evidencias/logro_evidencia.pdf');

-- ==========================================
-- PUBLICACIÓN-EVIDENCIA
-- ==========================================

INSERT INTO publicacion_evidencia (publicacion_id, evidencia_id) VALUES
(1, 1), -- Artículo trazabilidad
(2, 2), -- Dashboard screenshot
(3, 3), -- Coloquio certificado
(4, 4), -- Secuenciación reporte
(7, 5); -- Patente documento

-- ==========================================
-- COMENTARIOS
-- ==========================================

INSERT INTO comentario (publicacion_id, usuario_id, contenido) VALUES
(1, 6, '¡Felicitaciones! Es un gran logro para el semillero.'),
(1, 7, 'Excelente trabajo. ¿Pueden compartir el preprint?'),
(2, 2, 'El dashboard está quedando muy bien. Gran trabajo Juliana.'),
(2, 9, 'Me encanta el diseño. ¿Cuándo estará en producción?'),
(4, 5, '¡Increíble! ¿Qué especies están secuenciando?'),
(5, 5, '¿Necesitan ayuda con el dataset? Tengo experiencia con sklearn.'),
(7, 6, '¡Wow! Una patente. Eso es impresionante.'),
(8, 4, 'Buen trabajo David. El modelo es muy eficiente.'),
(10, 2, '¡Bienvenido Iván! Espero que te aprueben pronto.'),
(12, 8, '¡Felicidades a todo el equipo! Es un logro histórico.');

-- ==========================================
-- REACCIONES
-- ==========================================

INSERT INTO reaccion (publicacion_id, usuario_id, tipo) VALUES
(1, 6, 'me_gusta'),
(1, 7, 'me_encanta'),
(1, 2, 'me_gusta'),
(2, 9, 'me_gusta'),
(2, 5, 'me_encanta'),
(4, 5, 'me_gusta'),
(4, 8, 'me_interesa'),
(5, 6, 'me_gusta'),
(7, 5, 'me_encanta'),
(7, 9, 'me_gusta'),
(12, 5, 'me_encanta'),
(12, 7, 'me_gusta'),
(12, 8, 'me_gusta');

-- ==========================================
-- COMPARTIDOS
-- ==========================================

INSERT INTO compartido (publicacion_id, usuario_id) VALUES
(1, 6),
(1, 7),
(2, 9),
(4, 5),
(7, 5),
(12, 7);

-- ==========================================
-- SEGUIMIENTO USUARIO
-- ==========================================

INSERT INTO seguimiento_usuario (seguidor_id, seguido_id) VALUES
(5, 2), -- Juliana sigue a Docente
(5, 7), -- Juliana sigue a Laura
(6, 5), -- Camilo sigue a Juliana
(7, 5), -- Laura sigue a Juliana
(9, 5), -- Paula sigue a Juliana
(10, 5); -- Iván sigue a Juliana

-- ==========================================
-- SEGUIMIENTO SEMILLERO
-- ==========================================

INSERT INTO seguimiento_semillero (usuario_id, semillero_id) VALUES
(6, 1), -- Camilo sigue RIUL-Dev
(8, 2), -- David sigue BioUL
(9, 1), -- Paula sigue RIUL-Dev
(10, 1); -- Iván sigue RIUL-Dev

-- ==========================================
-- LOGROS
-- ==========================================

INSERT INTO logro (usuario_id, tipo, titulo, descripcion, estado, validado_por, fecha_validacion) VALUES
(5, 'articulo', 'Artículo aceptado en revista indexada', 'Artículo sobre trazabilidad académica aceptado en revista indexada.', 'aprobado', 1, '2026-09-15'),
(5, 'ponencia', 'Ponencia en congreso nacional', 'Ponencia presentada en Congreso Nacional de Ingeniería de Software.', 'aprobado', 1, '2026-08-20'),
(5, 'proyecto', 'Proyecto de predicción de deserción', 'Participación en proyecto de predicción de deserción estudiantil.', 'aprobado', 1, '2026-07-10'),
(6, 'proyecto', 'Sistema IoT para laboratorios', 'Desarrollo de sistema de monitoreo IoT.', 'enviado', NULL, NULL),
(7, 'articulo', 'Publicación en Nature', 'Artículo sobre genoma aceptado en Nature.', 'aprobado', 1, '2026-10-01'),
(7, 'ponencia', 'Conferencia internacional', 'Ponencia en conferencia internacional de bioinformática.', 'enviado', NULL, NULL),
(8, 'proyecto', 'Modelo matemático optimizado', 'Optimización de algoritmo de rutas logísticas.', 'aprobado', 1, '2026-09-20'),
(9, 'articulo', 'Primer artículo', 'Primer artículo aceptado para publicación.', 'rechazado', 1, '2026-09-25'),
(10, 'proyecto', 'Participación en proyecto', 'Solicitud de reconocimiento por participación en proyecto.', 'enviado', NULL, NULL);

-- ==========================================
-- LOGRO-EVIDENCIA
-- ==========================================

INSERT INTO logro_evidencia (logro_id, evidencia_id) VALUES
(1, 1), -- Artículo trazabilidad
(2, 3), -- Coloquio certificado
(5, 4); -- Secuenciación reporte

-- ==========================================
-- MOVIMIENTOS XP (basado en seed)
-- ==========================================

-- Insertar movimientos XP basados en el seed
-- Estos son calculados para reflejar los xp_total de los usuarios

-- Juliana (id=5, xp_total=1240)
INSERT INTO movimiento_xp (usuario_id, tipo_actividad_id, xp_ganada, referencia_tipo, referencia_id) VALUES
(5, 1, 50, 'usuario', 5), -- Registro
(5, 2, 100, 'semillero_integrante', 1), -- Vinculación
(5, 9, 300, 'logro', 1), -- Logro validado
(5, 9, 300, 'logro', 2), -- Logro validado
(5, 9, 300, 'logro', 3), -- Logro validado
(5, 3, 80, 'publicacion', 1), -- Publicación
(5, 3, 80, 'publicacion', 2), -- Publicación
(5, 3, 80, 'publicacion', 3), -- Publicación
(5, 6, 40, 'participacion_evento', 1), -- Evento
(5, 5, 150, 'proyecto', 1); -- Proyecto

-- Camilo (id=6, xp_total=980)
INSERT INTO movimiento_xp (usuario_id, tipo_actividad_id, xp_ganada, referencia_tipo, referencia_id) VALUES
(6, 1, 50, 'usuario', 6),
(6, 2, 100, 'semillero_integrante', 5),
(6, 3, 80, 'publicacion', 6),
(6, 4, 20, 'comentario', 1),
(6, 5, 10, 'reaccion', 1),
(6, 6, 40, 'participacion_evento', 2),
(6, 7, 150, 'proyecto', 4),
(6, 8, 200, 'producto', 6),
(6, 4, 20, 'comentario', 7),
(6, 5, 10, 'reaccion', 5),
(6, 5, 10, 'reaccion', 7),
(6, 5, 10, 'reaccion', 13);

-- Laura (id=7, xp_total=850)
INSERT INTO movimiento_xp (usuario_id, tipo_actividad_id, xp_ganada, referencia_tipo, referencia_id) VALUES
(7, 1, 50, 'usuario', 7),
(7, 2, 100, 'semillero_integrante', 2),
(7, 9, 300, 'logro', 5), -- Logro validado
(7, 3, 80, 'publicacion', 4),
(7, 4, 20, 'comentario', 1),
(7, 5, 10, 'reaccion', 1),
(7, 6, 40, 'participacion_evento', 1),
(7, 6, 40, 'participacion_evento', 5),
(7, 5, 10, 'reaccion', 4),
(7, 5, 10, 'reaccion', 12),
(7, 5, 10, 'reaccion', 13),
(7, 6, 40, 'participacion_evento', 10);

-- David (id=8, xp_total=720)
INSERT INTO movimiento_xp (usuario_id, tipo_actividad_id, xp_ganada, referencia_tipo, referencia_id) VALUES
(8, 1, 50, 'usuario', 8),
(8, 2, 100, 'semillero_integrante', 3),
(8, 9, 300, 'logro', 7), -- Logro validado
(8, 3, 80, 'publicacion', 8),
(8, 4, 20, 'comentario', 8),
(8, 6, 40, 'participacion_evento', 5),
(8, 6, 40, 'participacion_evento', 10),
(8, 5, 10, 'reaccion', 4),
(8, 5, 10, 'reaccion', 12),
(8, 5, 10, 'reaccion', 13);

-- Otros usuarios (XP básico)
INSERT INTO movimiento_xp (usuario_id, tipo_actividad_id, xp_ganada, referencia_tipo, referencia_id) VALUES
(9, 1, 50, 'usuario', 9),
(9, 2, 100, 'semillero_integrante', 2),
(9, 3, 80, 'publicacion', 10),
(9, 4, 20, 'comentario', 2),
(9, 4, 20, 'comentario', 3),
(9, 5, 10, 'reaccion', 2),
(9, 5, 10, 'reaccion', 7),
(9, 6, 40, 'participacion_evento', 3),
(9, 7, 150, 'proyecto', 1),
(9, 8, 200, 'producto', 1),
(10, 1, 50, 'usuario', 10),
(10, 3, 80, 'publicacion', 11),
(10, 4, 20, 'comentario', 10),
(10, 5, 10, 'reaccion', 7),
(10, 6, 40, 'participacion_evento', 3),
(10, 7, 150, 'proyecto', 1),
(10, 8, 200, 'producto', 1);

-- ==========================================
-- USUARIO-INSIGNIA
-- ==========================================

-- Juliana (id=5)
INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por) VALUES
(5, 1, NULL), -- Primeros pasos
(5, 3, NULL), -- 1000 XP
(5, 4, NULL); -- 5 logros validados

-- Laura (id=7)
INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por) VALUES
(7, 1, NULL),
(7, 3, NULL);

-- David (id=8)
INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por) VALUES
(8, 1, NULL);

-- Docentes (insignia de líder)
INSERT INTO usuario_insignia (usuario_id, insignia_id, otorgada_por) VALUES
(2, 6, NULL), -- Líder de semillero
(3, 6, NULL),
(4, 6, NULL);

-- ==========================================
-- NOTIFICACIONES
-- ==========================================

INSERT INTO notificacion (usuario_id, tipo, titulo, mensaje, referencia_tipo, referencia_id) VALUES
(5, 'logro_aprobado', 'Logro validado', 'Tu logro "Artículo aceptado en revista indexada" ha sido validado. ¡Has ganado XP!', 'logro', 1),
(5, 'logro_aprobado', 'Logro validado', 'Tu logro "Ponencia en congreso nacional" ha sido validado. ¡Has ganado XP!', 'logro', 2),
(5, 'vinculacion_aprobada', 'Vinculación aprobada', 'Tu solicitud de vinculación al semillero ha sido aprobada.', 'semillero_integrante', 1),
(7, 'vinculacion_aprobada', 'Vinculación aprobada', 'Tu solicitud de vinculación al semillero ha sido aprobada.', 'semillero_integrante', 2),
(6, 'vinculacion_rechazada', 'Vinculación rechazada', 'Tu solicitud de vinculación al semillero ha sido rechazada.', 'semillero_integrante', 5),
(10, 'vinculacion_solicitada', 'Solicitud de vinculación', 'Un nuevo estudiante ha solicitado vincularse a tu semillero.', 'semillero_integrante', 4),
(2, 'vinculacion_solicitada', 'Solicitud de vinculación', 'Un nuevo estudiante ha solicitado vincularse a tu semillero.', 'semillero_integrante', 4),
(5, 'nuevo_comentario', 'Nuevo comentario', 'Alguien comentó en tu publicación.', 'comentario', 1),
(5, 'nueva_reaccion', 'Nueva reacción', 'Alguien reaccionó a tu publicación.', 'reaccion', 1),
(7, 'nueva_publicacion', 'Nueva publicación', 'Juliana Díaz publicó algo nuevo.', 'publicacion', 1),
(9, 'cuenta_validada', 'Cuenta validada', 'Tu cuenta institucional ha sido validada. Ya puedes acceder a RIUL.', 'usuario', 9),
(5, 'convocatoria_publicada', 'Nueva convocatoria', 'Se ha publicado una nueva convocatoria: Semilleros de investigación aplicada 2026-II', 'convocatoria', 1);
