import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print("ERROR: DATABASE_URL not set.")
    exit(1)

url = urlparse(db_url)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port or 5432

sqlite_path = 'db.sqlite3'
if not os.path.exists(sqlite_path):
    sqlite_path = 'core_platform/db.sqlite3'

print(f"Reading SQLite: {sqlite_path}")
s_conn = sqlite3.connect(sqlite_path)
s_cursor = s_conn.cursor()

print("Connecting to Postgres...")
pg_conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
pg_cursor = pg_conn.cursor()

pg_cursor.execute("SET session_replication_role = 'replica';")

tables_order = [
    'quiz_engine_assignment',
    'quiz_engine_userprofile',
    'quiz_engine_answer',
    'quiz_engine_question',
    'quiz_engine_quiz',
    'quiz_engine_quiztheme',
    'quiz_engine_subject',
    'auth_user'
]

insert_order = list(reversed(tables_order))

for table in insert_order:
    try:
        s_cursor.execute(f"SELECT * FROM {table};")
    except Exception:
        continue
    
    rows = s_cursor.fetchall()
    if not rows:
        continue
    
    print(f"Migrating table with boolean casting: {table} ({len(rows)} rows)")
    s_cursor.execute(f"PRAGMA table_info({table});")
    col_info = s_cursor.fetchall()
    columns = [info[1] for info in col_info]
    col_types = [info[2].upper() for info in col_info]
    
    col_str = ", ".join([f'"{c}"' for c in columns])
    placeholders = ", ".join(["%s"] * len(columns))
    
    for row in rows:
        # Cast boolean integers (0/1) to Python bools for postgres boolean columns
        converted_row = []
        for val, ctype in zip(row, col_types):
            if 'BOOL' in ctype and val is not None:
                converted_row.append(bool(val))
            else:
                converted_row.append(val)
                
        try:
            pg_cursor.execute(f"INSERT INTO {table} ({col_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;", tuple(converted_row))
            pg_conn.commit()
        except Exception as e:
            pg_conn.rollback()
            print(f"Error in {table}: {e}")

pg_cursor.execute("SET session_replication_role = 'origin';")
pg_conn.commit()
s_conn.close()
pg_conn.close()
print("Full database migration with boolean casting completed successfully!")
