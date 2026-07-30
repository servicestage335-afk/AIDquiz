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

# Disable triggers/constraints temporarily or just insert cleanly
pg_cursor.execute("SET session_replication_role = 'replica';")

# 1. Migrate auth_user
s_cursor.execute("SELECT id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined FROM auth_user;")
users = s_cursor.fetchall()
print(f"Migrating {len(users)} users...")
for u in users:
    pg_cursor.execute("""
        INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET username=EXCLUDED.username, email=EXCLUDED.email, password=EXCLUDED.password;
    """, (u[0], u[1], u[2], bool(u[3]), u[4], u[5], u[6], u[7], bool(u[8]), bool(u[9]), u[10]))

# 2. Migrate quiz_engine_userprofile
try:
    s_cursor.execute("SELECT id, verification_code, verification_code_created_at, user_id FROM quiz_engine_userprofile;")
    profiles = s_cursor.fetchall()
    print(f"Migrating {len(profiles)} user profiles...")
    for p in profiles:
        pg_cursor.execute("""
            INSERT INTO quiz_engine_userprofile (id, verification_code, verification_code_created_at, user_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, p)
except Exception as e:
    print(f"Skipped userprofile: {e}")

# Re-enable constraints
pg_cursor.execute("SET session_replication_role = 'origin';")
pg_conn.commit()
s_conn.close()
pg_conn.close()
print("Users and profiles migration complete!")
