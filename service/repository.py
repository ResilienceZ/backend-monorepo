import psycopg
import os

def exec_select(query: str):
    conn = psycopg.connect(
        host = os.environ.get('DB_HOST'),
        user = os.environ.get('DB_USERNAME'),
        password = os.environ.get('DB_PASSWORD'),
        database = os.environ.get('DB_SCHEMA'),
    )
    
    cur = conn.cursor()
    
    cur.execute(query)
    
    result = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return result