import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config.database import get_connection, release_connection
from routes import auth_bp, publicaciones_bp, semilleros_bp, logros_bp, admin_bp, ranking_bp

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv('PORT', 3000))

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as error:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500
    finally:
        if conn:
            release_connection(conn)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(publicaciones_bp, url_prefix='/api/publicaciones')
app.register_blueprint(semilleros_bp, url_prefix='/api/semilleros')
app.register_blueprint(logros_bp, url_prefix='/api/logros')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(ranking_bp, url_prefix='/api/ranking')

# Error handling
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

if __name__ == '__main__':
    print(f'API RIUL corriendo en puerto {PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=False)
