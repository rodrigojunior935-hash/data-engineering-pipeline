import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="host.docker.internal",
        database="pipeline_db",
        user="postgres",
        password="postgres"
    )
    return conn
