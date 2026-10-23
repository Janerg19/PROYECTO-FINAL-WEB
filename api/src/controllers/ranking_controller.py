import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import request, jsonify
from config.database import get_connection, release_connection

def get_ranking_semilleros():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM v_ranking_semilleros')
        ranking = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in ranking]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener ranking semilleros: {e}')
        return jsonify({'error': 'Error al obtener ranking semilleros'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_ranking_investigadores():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM v_ranking_investigadores')
        ranking = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in ranking]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener ranking investigadores: {e}')
        return jsonify({'error': 'Error al obtener ranking investigadores'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_kpis():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM v_kpis_institucionales')
        kpis = cursor.fetchone()

        if kpis:
            column_names = [desc[0] for desc in cursor.description]
            result = dict(zip(column_names, kpis))
            return jsonify(result)
        else:
            return jsonify({})
    except Exception as e:
        print(f'Error al obtener KPIs: {e}')
        return jsonify({'error': 'Error al obtener KPIs'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_indicadores_facultad():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM v_indicadores_facultad')
        indicadores = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in indicadores]

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener indicadores facultad: {e}')
        return jsonify({'error': 'Error al obtener indicadores facultad'}), 500
    finally:
        if conn:
            release_connection(conn)

def get_hoja_vida(usuario_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM v_hoja_vida_investigativa WHERE usuario_id = %s',
            (usuario_id,)
        )
        hoja_vida = cursor.fetchone()

        if not hoja_vida:
            return jsonify({'error': 'Hoja de vida no encontrada'}), 404

        column_names = [desc[0] for desc in cursor.description]
        result = dict(zip(column_names, hoja_vida))

        return jsonify(result)
    except Exception as e:
        print(f'Error al obtener hoja de vida: {e}')
        return jsonify({'error': 'Error al obtener hoja de vida'}), 500
    finally:
        if conn:
            release_connection(conn)
