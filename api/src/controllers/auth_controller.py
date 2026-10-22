import os
import bcrypt
import jwt
from flask import request, jsonify, g
from datetime import datetime, timedelta
from config.database import get_connection, release_connection

JWT_SECRET = os.getenv('JWT_SECRET', 'cambiar_esto_en_produccion')
SALT_ROUNDS = 10

def register():
    data = request.get_json()
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    email = data.get('email')
    password = data.get('password')
    programa_id = data.get('programa_id')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si el email ya existe
        cursor.execute('SELECT id FROM usuario WHERE email = %s', (email,))
        if cursor.fetchone():
            return jsonify({'error': 'El email ya está registrado'}), 400

        # Hash de contraseña
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(SALT_ROUNDS)).decode('utf-8')

        # Insertar usuario (rol estudiante por defecto, estado pendiente)
        cursor.execute(
            """INSERT INTO usuario (rol_id, nombres, apellidos, email, password_hash, estado)
               VALUES (
                 (SELECT id FROM rol WHERE nombre = 'estudiante'),
                 %s, %s, %s, %s, 'pendiente'
               )
               RETURNING id, nombres, apellidos, email, estado""",
            (nombres, apellidos, email, password_hash)
        )
        usuario = cursor.fetchone()
        conn.commit()

        # Si se proporcionó programa, asociarlo
        if programa_id:
            cursor.execute(
                'INSERT INTO usuario_programa (usuario_id, programa_id, fecha_inicio, actual) VALUES (%s, %s, CURRENT_DATE, TRUE)',
                (usuario[0], programa_id)
            )
            conn.commit()

        return jsonify({
            'message': 'Registro exitoso. Espera validación del administrador.',
            'usuario': {
                'id': usuario[0],
                'nombres': usuario[1],
                'apellidos': usuario[2],
                'email': usuario[3],
                'estado': usuario[4],
            }
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error en registro: {e}')
        return jsonify({'error': 'Error al registrar usuario'}), 500
    finally:
        if conn:
            release_connection(conn)

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Buscar usuario por email
        cursor.execute(
            """SELECT u.id, u.nombres, u.apellidos, u.email, u.password_hash, u.estado, u.xp_total, u.nivel_id,
                      r.nombre as rol, n.numero as nivel_numero, n.estrellas
               FROM usuario u
               JOIN rol r ON u.rol_id = r.id
               LEFT JOIN nivel n ON u.nivel_id = n.id
               WHERE u.email = %s AND u.eliminado_en IS NULL""",
            (email,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({'error': 'Credenciales inválidas'}), 401

        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), usuario[4].encode('utf-8')):
            return jsonify({'error': 'Credenciales inválidas'}), 401

        # Verificar estado de cuenta
        if usuario[5] != 'aprobada':
            return jsonify({
                'error': 'Cuenta no aprobada',
                'estado': usuario[5],
            }), 403

        # Generar token JWT
        token = jwt.encode({
            'id': usuario[0],
            'email': usuario[3],
            'rol': usuario[8],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, JWT_SECRET, algorithm='HS256')

        return jsonify({
            'token': token,
            'usuario': {
                'id': usuario[0],
                'nombres': usuario[1],
                'apellidos': usuario[2],
                'email': usuario[3],
                'rol': usuario[8],
                'xp_total': usuario[6],
                'nivel': usuario[9],
                'estrellas': usuario[10],
            }
        })
    except Exception as e:
        print(f'Error en login: {e}')
        return jsonify({'error': 'Error al iniciar sesión'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_me():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT u.id, u.nombres, u.apellidos, u.email, u.xp_total, u.nivel_id,
                      r.nombre as rol, n.numero as nivel_numero, n.estrellas,
                      pi.biografia, pi.intereses, pi.orcid, pi.cvlac
               FROM usuario u
               JOIN rol r ON u.rol_id = r.id
               LEFT JOIN nivel n ON u.nivel_id = n.id
               LEFT JOIN perfil_investigador pi ON u.id = pi.usuario_id
               WHERE u.id = %s AND u.eliminado_en IS NULL""",
            (g.user['id'],)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Obtener insignias del usuario
        cursor.execute(
            """SELECT i.id, i.nombre, i.descripcion, i.icono, i.color
               FROM usuario_insignia ui
               JOIN insignia i ON ui.insignia_id = i.id
               WHERE ui.usuario_id = %s""",
            (g.user['id'],)
        )
        insignias = cursor.fetchall()

        return jsonify({
            'usuario': {
                'id': usuario[0],
                'nombres': usuario[1],
                'apellidos': usuario[2],
                'email': usuario[3],
                'xp_total': usuario[4],
                'nivel_id': usuario[5],
                'rol': usuario[6],
                'nivel': usuario[7],
                'estrellas': usuario[8],
                'biografia': usuario[9],
                'intereses': usuario[10],
                'orcid': usuario[11],
                'cvlac': usuario[12],
                'insignias': [{'id': i[0], 'nombre': i[1], 'descripcion': i[2], 'icono': i[3], 'color': i[4]} for i in insignias]
            }
        })
    except Exception as e:
        print(f'Error al obtener usuario: {e}')
        return jsonify({'error': 'Error al obtener usuario'}), 500
    finally:
        if conn:
            release_connection(conn)
