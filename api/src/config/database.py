import os
import psycopg2
from psycopg2 import pool

db_host = os.getenv('DB_HOST', 'riul-db')
db_port = int(os.getenv('DB_PORT', 5432))
db_name = os.getenv('DB_NAME', 'riul')
db_user = os.getenv('DB_USER', 'riul_app')
db_password = os.getenv('DB_PASSWORD', 'cambiar_esto_en_produccion')

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)

def close_all_connections():
    connection_pool.closeall()
