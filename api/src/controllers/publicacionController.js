import pool from '../config/database.js';

export const getPublicaciones = async (req, res) => {
  try {
    const { limit = 20, offset = 0 } = req.query;

    const result = await pool.query(
      `SELECT p.id, p.titulo, p.contenido, p.creado_en,
              cp.nombre as categoria, cp.color as categoria_color,
              u.nombres, u.apellidos,
              s.nombre as semillero_nombre
       FROM publicacion p
       JOIN categoria_publicacion cp ON p.categoria_id = cp.id
       JOIN usuario u ON p.usuario_id = u.id
       LEFT JOIN semillero s ON p.semillero_id = s.id
       WHERE p.eliminado_en IS NULL
       ORDER BY p.creado_en DESC
       LIMIT $1 OFFSET $2`,
      [limit, offset]
    );

    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener publicaciones:', error);
    res.status(500).json({ error: 'Error al obtener publicaciones' });
  }
};

export const createPublicacion = async (req, res) => {
  const { categoria_id, titulo, contenido, semillero_id } = req.body;

  try {
    // Llamar a función de BD que inserta y da XP
    const result = await pool.query(
      'SELECT registrar_publicacion($1, $2, $3, $4, $5) as publicacion_id',
      [req.user.id, categoria_id, titulo, contenido, semillero_id || null]
    );

    res.status(201).json({
      message: 'Publicación creada exitosamente',
      publicacion_id: result.rows[0].publicacion_id,
    });
  } catch (error) {
    console.error('Error al crear publicación:', error);
    res.status(500).json({ error: 'Error al crear publicación' });
  }
};

export const comentar = async (req, res) => {
  const { publicacion_id, contenido } = req.body;

  try {
    const result = await pool.query(
      'SELECT comentar_publicacion($1, $2, $3) as comentario_id',
      [publicacion_id, req.user.id, contenido]
    );

    res.status(201).json({
      message: 'Comentario agregado',
      comentario_id: result.rows[0].comentario_id,
    });
  } catch (error) {
    console.error('Error al comentar:', error);
    res.status(500).json({ error: 'Error al comentar' });
  }
};

export const reaccionar = async (req, res) => {
  const { publicacion_id, tipo } = req.body;

  try {
    const result = await pool.query(
      'SELECT reaccionar_publicacion($1, $2, $3) as reaccion_id',
      [publicacion_id, req.user.id, tipo]
    );

    res.status(201).json({
      message: 'Reacción registrada',
      reaccion_id: result.rows[0].reaccion_id,
    });
  } catch (error) {
    console.error('Error al reaccionar:', error);
    res.status(500).json({ error: 'Error al reaccionar' });
  }
};

export const compartir = async (req, res) => {
  const { publicacion_id } = req.body;

  try {
    await pool.query(
      'INSERT INTO compartido (publicacion_id, usuario_id) VALUES ($1, $2) ON CONFLICT DO NOTHING',
      [publicacion_id, req.user.id]
    );

    res.json({ message: 'Publicación compartida' });
  } catch (error) {
    console.error('Error al compartir:', error);
    res.status(500).json({ error: 'Error al compartir' });
  }
};
