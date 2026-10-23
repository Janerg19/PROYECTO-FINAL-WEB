import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import request, jsonify, g
from config.database import get_connection, release_connection

def get_logros_pendientes():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM v_logros_pendientes')
        logros = cursor.fetchall()

        # Convertir filas a diccionarios (usando nombres de columnas)
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in logros]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener logros pendientes: {e}')
        return jsonify({'error': 'Error al obtener logros pendientes'}), 500
    finally:
        if conn:
            release_connection(conn)

def enviar_logro():
    data = request.get_json()
    tipo = data.get('tipo')
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO logro (usuario_id, tipo, titulo, descripcion, estado)
               VALUES (%s, %s, %s, %s, 'enviado')
               RETURNING id""",
            (g.user['id'], tipo, titulo, descripcion)
        )
        result = cursor.fetchone()
        conn.commit()

        return jsonify({
            'message': 'Logro enviado a validación',
            'logro_id': result[0]
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al enviar logro: {e}')
        return jsonify({'error': 'Error al enviar logro'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_mis_logros():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT l.id, l.tipo, l.titulo, l.descripcion, l.estado, l.fecha_validacion,
                      le.nombre_archivo, le.ruta
               FROM logro l
               LEFT JOIN logro_evidencia lee ON l.id = lee.logro_id
               LEFT JOIN evidencia le ON lee.evidencia_id = le.id
               WHERE l.usuario_id = %s
               ORDER BY l.creado_en DESC""",
            (g.user['id'],)
        )

        logros = cursor.fetchall()
        result = [
            {
                'id': l[0],
                'tipo': l[1],
                'titulo': l[2],
                'descripcion': l[3],
                'estado': l[4],
                'fecha_validacion': l[5].isoformat() if l[5] else None,
                'nombre_archivo': l[6],
                'ruta': l[7]
            }
            for l in logros
        ]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener logros: {e}')
        return jsonify({'error': 'Error al obtener logros'}), 500
    finally:
        if conn:
            release_connection(conn)

def aprobar_logro(logro_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE logro
               SET estado = 'aprobado', validado_por = %s, fecha_validacion = CURRENT_TIMESTAMP
               WHERE id = %s""",
            (g.user['id'], logro_id)
        )
        conn.commit()

        return jsonify({'message': 'Logro aprobado'})
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al aprobar logro: {e}')
        return jsonify({'error': 'Error al aprobar logro'}), 500
    finally:
        if conn:
            release_connection(conn)

def rechazar_logro(logro_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE logro
               SET estado = 'rechazado', validado_por = %s, fecha_validacion = CURRENT_TIMESTAMP
               WHERE id = %s""",
            (g.user['id'], logro_id)
        )
        conn.commit()

        return jsonify({'message': 'Logro rechazado'})
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al rechazar logro: {e}')
        return jsonify({'error': 'Error al rechazar logro'}), 500
    finally:
        if conn:
            release_connection(conn)
