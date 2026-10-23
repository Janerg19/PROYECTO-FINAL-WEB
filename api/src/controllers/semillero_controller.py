import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import request, jsonify, g
from config.database import get_connection, release_connection

def get_semilleros():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT s.id, s.nombre, s.descripcion, s.fecha_creacion, s.activo,
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
               ORDER BY s.nombre"""
        )

        semilleros = cursor.fetchall()
        result = [
            {
                'id': s[0],
                'nombre': s[1],
                'descripcion': s[2],
                'fecha_creacion': s[3].isoformat() if s[3] else None,
                'activo': s[4],
                'facultad': s[5],
                'programa': s[6],
                'lider_nombres': s[7],
                'lider_apellidos': s[8],
                'num_integrantes': s[9]
            }
            for s in semilleros
        ]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener semilleros: {e}')
        return jsonify({'error': 'Error al obtener semilleros'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_semillero_by_id(id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT s.id, s.nombre, s.descripcion, s.fecha_creacion, s.activo,
                      f.nombre as facultad, p.nombre as programa,
                      u.nombres as lider_nombres, u.apellidos as lider_apellidos, u.email as lider_email
               FROM semillero s
               LEFT JOIN facultad f ON s.facultad_id = f.id
               LEFT JOIN programa p ON s.programa_id = p.id
               LEFT JOIN usuario u ON s.lider_id = u.id
               WHERE s.id = %s AND s.eliminado_en IS NULL""",
            (id,)
        )

        semillero = cursor.fetchone()

        if not semillero:
            return jsonify({'error': 'Semillero no encontrado'}), 404

        return jsonify({
            'id': semillero[0],
            'nombre': semillero[1],
            'descripcion': semillero[2],
            'fecha_creacion': semillero[3].isoformat() if semillero[3] else None,
            'activo': semillero[4],
            'facultad': semillero[5],
            'programa': semillero[6],
            'lider_nombres': semillero[7],
            'lider_apellidos': semillero[8],
            'lider_email': semillero[9]
        })
    except Exception as e:
        print(f'Error al obtener semillero: {e}')
        return jsonify({'error': 'Error al obtener semillero'}), 500
    finally:
        if conn:
            release_connection(conn)

def solicitar_vinculacion():
    data = request.get_json()
    semillero_id = data.get('semillero_id')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT solicitar_vinculacion(%s, %s) as vinculacion_id',
            (semillero_id, g.user['id'])
        )
        result = cursor.fetchone()
        conn.commit()

        return jsonify({
            'message': 'Solicitud de vinculación enviada',
            'vinculacion_id': result[0]
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al solicitar vinculación: {e}')
        if 'ya tiene una vinculación' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': 'Error al solicitar vinculación'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_integrantes(id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT si.id, si.rol, si.estado, si.fecha_solicitud, si.fecha_resolucion,
                      u.nombres, u.apellidos, u.email, u.xp_total, n.numero as nivel
               FROM semillero_integrante si
               JOIN usuario u ON si.usuario_id = u.id
               LEFT JOIN nivel n ON u.nivel_id = n.id
               WHERE si.semillero_id = %s
               ORDER BY si.estado, si.fecha_solicitud DESC""",
            (id,)
        )

        integrantes = cursor.fetchall()
        result = [
            {
                'id': i[0],
                'rol': i[1],
                'estado': i[2],
                'fecha_solicitud': i[3].isoformat() if i[3] else None,
                'fecha_resolucion': i[4].isoformat() if i[4] else None,
                'nombres': i[5],
                'apellidos': i[6],
                'email': i[7],
                'xp_total': i[8],
                'nivel': i[9]
            }
            for i in integrantes
        ]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener integrantes: {e}')
        return jsonify({'error': 'Error al obtener integrantes'}), 500
    finally:
        if conn:
            release_connection(conn)

def resolver_vinculacion():
    data = request.get_json()
    vinculacion_id = data.get('vinculacion_id')
    resolucion = data.get('resolucion')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT resolver_vinculacion(%s, %s, %s)',
            (vinculacion_id, resolucion, g.user['id'])
        )
        conn.commit()

        return jsonify({'message': f'Vinculación {resolucion}'})
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al resolver vinculación: {e}')
        return jsonify({'error': 'Error al resolver vinculación'}), 500
    finally:
        if conn:
            release_connection(conn)
