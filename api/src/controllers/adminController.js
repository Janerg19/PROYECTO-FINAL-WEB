import pool from '../config/database.js';

export const getCuentasPendientes = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM v_cuentas_pendientes');
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener cuentas pendientes:', error);
    res.status(500).json({ error: 'Error al obtener cuentas pendientes' });
  }
};

export const aprobarCuenta = async (req, res) => {
  const { usuario_id } = req.params;

  try {
    await pool.query('SELECT validar_cuenta($1, $2)', [usuario_id, req.user.id]);
    res.json({ message: 'Cuenta aprobada' });
  } catch (error) {
    console.error('Error al aprobar cuenta:', error);
    res.status(500).json({ error: 'Error al aprobar cuenta' });
  }
};

export const rechazarCuenta = async (req, res) => {
  const { usuario_id } = req.params;

  try {
    await pool.query(
      `UPDATE usuario SET estado = 'rechazada' WHERE id = $1`,
      [usuario_id]
    );
    res.json({ message: 'Cuenta rechazada' });
  } catch (error) {
    console.error('Error al rechazar cuenta:', error);
    res.status(500).json({ error: 'Error al rechazar cuenta' });
  }
};

export const getFacultades = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM facultad ORDER BY nombre');
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener facultades:', error);
    res.status(500).json({ error: 'Error al obtener facultades' });
  }
};

export const getProgramas = async (req, res) => {
  try {
    const { facultad_id } = req.query;

    let query = `
      SELECT p.id, p.nombre, p.codigo, p.tipo, f.nombre as facultad
      FROM programa p
      JOIN facultad f ON p.facultad_id = f.id
    `;
    const params = [];

    if (facultad_id) {
      query += ' WHERE p.facultad_id = $1';
      params.push(facultad_id);
    }

    query += ' ORDER BY p.nombre';

    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener programas:', error);
    res.status(500).json({ error: 'Error al obtener programas' });
  }
};
