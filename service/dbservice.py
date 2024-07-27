import psycopg2
import os

def exec_select(query: str, values: any):
    result = None
    try:
        with psycopg2.connect(
            host = os.environ.get('DB_HOST'),
            user = os.environ.get('DB_USERNAME'),
            password = os.environ.get('DB_PASSWORD'),
            database = os.environ.get('DB_SCHEMA'),
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
                result = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error) 
    return result

def exec_commit(query: str, values: any):
    try:
        with psycopg2.connect(
            host = os.environ.get('DB_HOST'),
            user = os.environ.get('DB_USERNAME'),
            password = os.environ.get('DB_PASSWORD'),
            database = os.environ.get('DB_SCHEMA'),
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error) 