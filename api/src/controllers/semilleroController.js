import pool from '../config/database.js';

export const getSemilleros = async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT s.id, s.nombre, s.descripcion, s.fecha_creacion, s.activo,
              f.nombre as facultad, p.nombre as programa,
              u.nombres as lider_nombres, u.apellidos as lider_apellidos,
              COUNT(DISTINCT si.usuario_id) as num_integrantes
       FROM semillero s
       LEFT JOIN facultad f ON s.facultad_id = f.id
       LEFT JOIN programa p ON s.programa_id = p.id
       LEFT JOIN usuario u ON s.lider_id = u.id
       LEFT JOIN semillero_integrante si ON s.id = si.semillero_id AND si.estado = 'aprobada'
       WHERE s.eliminado_en IS NULL
       GROUP BY s.id, s.nombre, s.descripcion, s.fecha_creacion, s.activo,
                f.nombre, p.nombre, u.nombres, u.apellidos
       ORDER BY s.nombre`
    );

    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener semilleros:', error);
    res.status(500).json({ error: 'Error al obtener semilleros' });
  }
};

export const getSemilleroById = async (req, res) => {
  const { id } = req.params;

  try {
    const result = await pool.query(
      `SELECT s.id, s.nombre, s.descripcion, s.fecha_creacion, s.activo,
              f.nombre as facultad, p.nombre as programa,
              u.nombres as lider_nombres, u.apellidos as lider_apellidos, u.email as lider_email
       FROM semillero s
       LEFT JOIN facultad f ON s.facultad_id = f.id
       LEFT JOIN programa p ON s.programa_id = p.id
       LEFT JOIN usuario u ON s.lider_id = u.id
       WHERE s.id = $1 AND s.eliminado_en IS NULL`,
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Semillero no encontrado' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error al obtener semillero:', error);
    res.status(500).json({ error: 'Error al obtener semillero' });
  }
};

export const solicitarVinculacion = async (req, res) => {
  const { semillero_id } = req.body;

  try {
    const result = await pool.query(
      'SELECT solicitar_vinculacion($1, $2) as vinculacion_id',
      [semillero_id, req.user.id]
    );

    res.status(201).json({
      message: 'Solicitud de vinculación enviada',
      vinculacion_id: result.rows[0].vinculacion_id,
    });
  } catch (error) {
    console.error('Error al solicitar vinculación:', error);
    if (error.message.includes('ya tiene una vinculación')) {
      res.status(400).json({ error: error.message });
    } else {
      res.status(500).json({ error: 'Error al solicitar vinculación' });
    }
  }
};

export const getIntegrantes = async (req, res) => {
  const { id } = req.params;

  try {
    const result = await pool.query(
      `SELECT si.id, si.rol, si.estado, si.fecha_solicitud, si.fecha_resolucion,
              u.nombres, u.apellidos, u.email, u.xp_total, n.numero as nivel
       FROM semillero_integrante si
       JOIN usuario u ON si.usuario_id = u.id
       LEFT JOIN nivel n ON u.nivel_id = n.id
       WHERE si.semillero_id = $1
       ORDER BY si.estado, si.fecha_solicitud DESC`,
      [id]
    );

    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener integrantes:', error);
    res.status(500).json({ error: 'Error al obtener integrantes' });
  }
};

export const resolverVinculacion = async (req, res) => {
  const { vinculacion_id, resolucion } = req.body;

  try {
    await pool.query(
      'SELECT resolver_vinculacion($1, $2, $3)',
      [vinculacion_id, resolucion, req.user.id]
    );

    res.json({ message: `Vinculación ${resolucion}` });
  } catch (error) {
    console.error('Error al resolver vinculación:', error);
    res.status(500).json({ error: 'Error al resolver vinculación' });
  }
};
