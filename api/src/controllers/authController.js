import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import pool from '../config/database.js';

const JWT_SECRET = process.env.JWT_SECRET || 'cambiar_esto_en_produccion';
const SALT_ROUNDS = 10;

export const register = async (req, res) => {
  const { nombres, apellidos, email, password, programa_id } = req.body;

  try {
    // Verificar si el email ya existe
    const existingUser = await pool.query(
      'SELECT id FROM usuario WHERE email = $1',
      [email]
    );

    if (existingUser.rows.length > 0) {
      return res.status(400).json({ error: 'El email ya está registrado' });
    }

    // Hash de contraseña
    const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);

    // Insertar usuario (rol estudiante por defecto, estado pendiente)
    const result = await pool.query(
      `INSERT INTO usuario (rol_id, nombres, apellidos, email, password_hash, estado)
       VALUES (
         (SELECT id FROM rol WHERE nombre = 'estudiante'),
         $1, $2, $3, $4, 'pendiente'
       )
       RETURNING id, nombres, apellidos, email, estado`,
      [nombres, apellidos, email, passwordHash]
    );

    const usuario = result.rows[0];

    // Si se proporcionó programa, asociarlo
    if (programa_id) {
      await pool.query(
        'INSERT INTO usuario_programa (usuario_id, programa_id, fecha_inicio, actual) VALUES ($1, $2, CURRENT_DATE, TRUE)',
        [usuario.id, programa_id]
      );
    }

    res.status(201).json({
      message: 'Registro exitoso. Espera validación del administrador.',
      usuario: {
        id: usuario.id,
        nombres: usuario.nombres,
        apellidos: usuario.apellidos,
        email: usuario.email,
        estado: usuario.estado,
      },
    });
  } catch (error) {
    console.error('Error en registro:', error);
    res.status(500).json({ error: 'Error al registrar usuario' });
  }
};

export const login = async (req, res) => {
  const { email, password } = req.body;

  try {
    // Buscar usuario por email
    const result = await pool.query(
      `SELECT u.id, u.nombres, u.apellidos, u.email, u.password_hash, u.estado, u.xp_total, u.nivel_id,
              r.nombre as rol, n.numero as nivel_numero, n.estrellas
       FROM usuario u
       JOIN rol r ON u.rol_id = r.id
       LEFT JOIN nivel n ON u.nivel_id = n.id
       WHERE u.email = $1 AND u.eliminado_en IS NULL`,
      [email]
    );

    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Credenciales inválidas' });
    }

    const usuario = result.rows[0];

    // Verificar contraseña
    const validPassword = await bcrypt.compare(password, usuario.password_hash);

    if (!validPassword) {
      return res.status(401).json({ error: 'Credenciales inválidas' });
    }

    // Verificar estado de cuenta
    if (usuario.estado !== 'aprobada') {
      return res.status(403).json({
        error: 'Cuenta no aprobada',
        estado: usuario.estado,
      });
    }

    // Generar token JWT
    const token = jwt.sign(
      {
        id: usuario.id,
        email: usuario.email,
        rol: usuario.rol,
      },
      JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({
      token,
      usuario: {
        id: usuario.id,
        nombres: usuario.nombres,
        apellidos: usuario.apellidos,
        email: usuario.email,
        rol: usuario.rol,
        xp_total: usuario.xp_total,
        nivel: usuario.nivel_numero,
        estrellas: usuario.estrellas,
      },
    });
  } catch (error) {
    console.error('Error en login:', error);
    res.status(500).json({ error: 'Error al iniciar sesión' });
  }
};

export const getMe = async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT u.id, u.nombres, u.apellidos, u.email, u.xp_total, u.nivel_id,
              r.nombre as rol, n.numero as nivel_numero, n.estrellas,
              pi.biografia, pi.intereses, pi.orcid, pi.cvlac
       FROM usuario u
       JOIN rol r ON u.rol_id = r.id
       LEFT JOIN nivel n ON u.nivel_id = n.id
       LEFT JOIN perfil_investigador pi ON u.id = pi.usuario_id
       WHERE u.id = $1 AND u.eliminado_en IS NULL`,
      [req.user.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }

    const usuario = result.rows[0];

    // Obtener insignias del usuario
    const insigniasResult = await pool.query(
      `SELECT i.id, i.nombre, i.descripcion, i.icono, i.color
       FROM usuario_insignia ui
       JOIN insignia i ON ui.insignia_id = i.id
       WHERE ui.usuario_id = $1`,
      [req.user.id]
    );

    res.json({
      usuario: {
        ...usuario,
        insignias: insigniasResult.rows,
      },
    });
  } catch (error) {
    console.error('Error al obtener usuario:', error);
    res.status(500).json({ error: 'Error al obtener usuario' });
  }
};
