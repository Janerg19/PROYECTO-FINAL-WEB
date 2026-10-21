import pool from '../config/database.js';

export const getLogrosPendientes = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM v_logros_pendientes');
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener logros pendientes:', error);
    res.status(500).json({ error: 'Error al obtener logros pendientes' });
  }
};

export const enviarLogro = async (req, res) => {
  const { tipo, titulo, descripcion } = req.body;

  try {
    const result = await pool.query(
      `INSERT INTO logro (usuario_id, tipo, titulo, descripcion, estado)
       VALUES ($1, $2, $3, $4, 'enviado')
       RETURNING id`,
      [req.user.id, tipo, titulo, descripcion]
    );

    res.status(201).json({
      message: 'Logro enviado a validación',
      logro_id: result.rows[0].id,
    });
  } catch (error) {
    console.error('Error al enviar logro:', error);
    res.status(500).json({ error: 'Error al enviar logro' });
  }
};

export const getMisLogros = async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT l.id, l.tipo, l.titulo, l.descripcion, l.estado, l.fecha_validacion,
              le.nombre_archivo, le.ruta
       FROM logro l
       LEFT JOIN logro_evidencia lee ON l.id = lee.logro_id
       LEFT JOIN evidencia le ON lee.evidencia_id = le.id
       WHERE l.usuario_id = $1
       ORDER BY l.creado_en DESC`,
      [req.user.id]
    );

    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener logros:', error);
    res.status(500).json({ error: 'Error al obtener logros' });
  }
};

export const aprobarLogro = async (req, res) => {
  const { logro_id } = req.params;

  try {
    await pool.query(
      `UPDATE logro
       SET estado = 'aprobado', validado_por = $1, fecha_validacion = CURRENT_TIMESTAMP
       WHERE id = $2`,
      [req.user.id, logro_id]
    );

    res.json({ message: 'Logro aprobado' });
  } catch (error) {
    console.error('Error al aprobar logro:', error);
    res.status(500).json({ error: 'Error al aprobar logro' });
  }
};

export const rechazarLogro = async (req, res) => {
  const { logro_id } = req.params;

  try {
    await pool.query(
      `UPDATE logro
       SET estado = 'rechazado', validado_por = $1, fecha_validacion = CURRENT_TIMESTAMP
       WHERE id = $2`,
      [req.user.id, logro_id]
    );

    res.json({ message: 'Logro rechazado' });
  } catch (error) {
    console.error('Error al rechazar logro:', error);
    res.status(500).json({ error: 'Error al rechazar logro' });
  }
};
