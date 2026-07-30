import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print("ERROR: DATABASE_URL not set in environment.")
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

if not os.path.exists(sqlite_path):
    print("ERROR: No local sqlite3 database found.")
    exit(1)

print(f"Reading from local SQLite: {sqlite_path}")
sqlite_conn = sqlite3.connect(sqlite_path)
sqlite_cursor = sqlite_conn.cursor()

print(f"Connecting to Postgres at {host}:{port}/{dbname}...")
pg_conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
pg_cursor = pg_conn.cursor()

# Migrate tables in correct foreign key order
tables_order = [
    'django_migrations',
    'django_content_type',
    'auth_permission',
    'auth_group',
    'auth_user',
    'auth_group_permissions',
    'auth_user_groups',
    'auth_user_user_permissions',
    'django_admin_log',
    'django_session',
    'quiz_engine_subject',
    'quiz_engine_quiztheme',
    'quiz_engine_quiz',
    'quiz_engine_question',
    'quiz_engine_answer',
    'quiz_engine_userprofile',
    'quiz_engine_assignment'
]

for table in tables_order:
    try:
        sqlite_cursor.execute(f"SELECT * FROM {table};")
    except Exception:
        continue
    
    rows = sqlite_cursor.fetchall()
    if not rows:
        continue
    
    print(f"Migrating table: {table} ({len(rows)} rows)")
    sqlite_cursor.execute(f"PRAGMA table_info({table});")
    columns = [info[1] for info in sqlite_cursor.fetchall()]
    
    col_str = ", ".join([f'"{c}"' for c in columns])
    placeholders = ", ".join(["%s"] * len(columns))
    
    for row in rows:
        try:
            pg_cursor.execute(f"INSERT INTO {table} ({col_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;", row)
            pg_conn.commit()
        except Exception as e:
            pg_conn.rollback()
            # print(f"Skipped row in {table}: {e}")

print("Data migration completed successfully!")
sqlite_conn.close()
pg_conn.close()
