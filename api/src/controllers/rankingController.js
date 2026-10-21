import pool from '../config/database.js';

export const getRankingSemilleros = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM v_ranking_semilleros');
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener ranking semilleros:', error);
    res.status(500).json({ error: 'Error al obtener ranking semilleros' });
  }
};

export const getRankingInvestigadores = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM v_ranking_investigadores');
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener ranking investigadores:', error);
    res.status(500).json({ error: 'Error al obtener ranking investigadores' });
  }
};

export const getKPIs = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM v_kpis_institucionales');
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error al obtener KPIs:', error);
    res.status(500).json({ error: 'Error al obtener KPIs' });
  }
};

export const getIndicadoresFacultad = async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM v_indicadores_facultad');
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener indicadores facultad:', error);
    res.status(500).json({ error: 'Error al obtener indicadores facultad' });
  }
};

export const getHojaVida = async (req, res) => {
  const { usuario_id } = req.params;

  try {
    const result = await pool.query(
      'SELECT * FROM v_hoja_vida_investigativa WHERE usuario_id = $1',
      [usuario_id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Hoja de vida no encontrada' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error al obtener hoja de vida:', error);
    res.status(500).json({ error: 'Error al obtener hoja de vida' });
  }
};
