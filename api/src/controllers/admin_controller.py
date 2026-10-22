from flask import request, jsonify, g
from config.database import get_connection, release_connection

def get_cuentas_pendientes():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM v_cuentas_pendientes')
        cuentas = cursor.fetchall()

        # Convertir filas a diccionarios
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in cuentas]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener cuentas pendientes: {e}')
        return jsonify({'error': 'Error al obtener cuentas pendientes'}), 500
    finally:
        if conn:
            release_connection(conn)

def aprobar_cuenta(usuario_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT validar_cuenta(%s, %s)', (usuario_id, g.user['id']))
        conn.commit()

        return jsonify({'message': 'Cuenta aprobada'})
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al aprobar cuenta: {e}')
        return jsonify({'error': 'Error al aprobar cuenta'}), 500
    finally:
        if conn:
            release_connection(conn)

def rechazar_cuenta(usuario_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE usuario SET estado = 'rechazada' WHERE id = %s""",
            (usuario_id,)
        )
        conn.commit()

        return jsonify({'message': 'Cuenta rechazada'})
    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error al rechazar cuenta: {e}')
        return jsonify({'error': 'Error al rechazar cuenta'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_facultades():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM facultad ORDER BY nombre')
        facultades = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in facultades]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener facultades: {e}')
        return jsonify({'error': 'Error al obtener facultades'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_programas():
    facultad_id = request.args.get('facultad_id')

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT p.id, p.nombre, p.codigo, p.tipo, f.nombre as facultad
            FROM programa p
            JOIN facultad f ON p.facultad_id = f.id
        """
        params = []

        if facultad_id:
            query += ' WHERE p.facultad_id = %s'
            params.append(facultad_id)

        query += ' ORDER BY p.nombre'

        cursor.execute(query, params)
        programas = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in programas]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener programas: {e}')
        return jsonify({'error': 'Error al obtener programas'}), 500
    finally:
        if conn:
            release_connection(conn)
