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

# Get users from SQLite
s_cursor.execute("SELECT id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined FROM auth_user;")
users = s_cursor.fetchall()
print(f"Found {len(users)} users in SQLite.")

for u in users:
    print(f"Migrating user: {u[4]} (email: {u[7]})")
    pg_cursor.execute("""
        INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET username=EXCLUDED.username, email=EXCLUDED.email, password=EXCLUDED.password;
    """, u)

pg_conn.commit()
s_conn.close()
pg_conn.close()
print("User migration complete!")
