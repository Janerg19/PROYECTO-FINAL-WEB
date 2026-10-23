import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import request, jsonify, g
from config.database import get_connection, release_connection

def get_publicaciones():
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT p.id, p.titulo, p.contenido, p.creado_en,
                      cp.nombre as categoria, cp.color as categoria_color,
                      u.nombres, u.apellidos,
                      s.nombre as semillero_nombre
               FROM publicacion p
               JOIN categoria_publicacion cp ON p.categoria_id = cp.id
               JOIN usuario u ON p.usuario_id = u.id
               LEFT JOIN semillero s ON p.semillero_id = s.id
               WHERE p.eliminado_en IS NULL
               ORDER BY p.creado_en DESC
               LIMIT %s OFFSET %s""",
            (limit, offset)
        )

        publicaciones = cursor.fetchall()
        result = [
            {
                'id': p[0],
                'titulo': p[1],
                'contenido': p[2],
                'creado_en': p[3].isoformat() if p[3] else None,
                'categoria': p[4],
                'categoria_color': p[5],
                'nombres': p[6],
                'apellidos': p[7],
                'semillero_nombre': p[8]
            }
            for p in publicaciones
        ]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener publicaciones: {e}')
        return jsonify({'error': 'Error al obtener publicaciones'}), 500
    finally:
        if conn:
            release_connection(conn)

def create_publicacion():
    data = request.get_json()
    categoria_id = data.get('categoria_id')
    titulo = data.get('titulo')
    contenido = data.get('contenido')
    semillero_id = data.get('semillero_id')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Llamar a función de BD que inserta y da XP
        cursor.execute(
            'SELECT registrar_publicacion(%s, %s, %s, %s, %s) as publicacion_id',
            (g.user['id'], categoria_id, titulo, contenido, semillero_id or None)
        )
        result = cursor.fetchone()
        conn.commit()

        return jsonify({
            'message': 'Publicación creada exitosamente',
            'publicacion_id': result[0]
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al crear publicación: {e}')
        return jsonify({'error': 'Error al crear publicación'}), 500
    finally:
        if conn:
            release_connection(conn)

def comentar():
    data = request.get_json()
    publicacion_id = data.get('publicacion_id')
    contenido = data.get('contenido')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT comentar_publicacion(%s, %s, %s) as comentario_id',
            (publicacion_id, g.user['id'], contenido)
        )
        result = cursor.fetchone()
        conn.commit()

        return jsonify({
            'message': 'Comentario agregado',
            'comentario_id': result[0]
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al comentar: {e}')
        return jsonify({'error': 'Error al comentar'}), 500
    finally:
        if conn:
            release_connection(conn)

def reaccionar():
    data = request.get_json()
    publicacion_id = data.get('publicacion_id')
    tipo = data.get('tipo')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT reaccionar_publicacion(%s, %s, %s) as reaccion_id',
            (publicacion_id, g.user['id'], tipo)
        )
        result = cursor.fetchone()
        conn.commit()

        return jsonify({
            'message': 'Reacción registrada',
            'reaccion_id': result[0]
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al reaccionar: {e}')
        return jsonify({'error': 'Error al reaccionar'}), 500
    finally:
        if conn:
            release_connection(conn)

def compartir():
    data = request.get_json()
    publicacion_id = data.get('publicacion_id')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO compartido (publicacion_id, usuario_id)
               VALUES (%s, %s)
               ON CONFLICT DO NOTHING""",
            (publicacion_id, g.user['id'])
        )
        conn.commit()

        return jsonify({'message': 'Publicación compartida'})
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al compartir: {e}')
        return jsonify({'error': 'Error al compartir'}), 500
    finally:
        if conn:
            release_connection(conn)
