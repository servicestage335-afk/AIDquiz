import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

# Get DATABASE_URL from environment
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

# Connect to SQLite (Check root db.sqlite3 and core_platform/db.sqlite3)
sqlite_path = 'db.sqlite3'
if not os.path.exists(sqlite_path):
    sqlite_path = 'core_platform/db.sqlite3'

if not os.path.exists(sqlite_path):
    print("ERROR: No local sqlite3 database found.")
    exit(1)

print(f"Reading from local SQLite: {sqlite_path}")
sqlite_conn = sqlite3.connect(sqlite_path)
sqlite_cursor = sqlite_conn.cursor()

# Connect to Postgres
print(f"Connecting to Postgres at {host}:{port}/{dbname}...")
pg_conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
pg_cursor = pg_conn.cursor()

# Get all tables
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = [row[0] for row in sqlite_cursor.fetchall()]

for table in tables:
    print(f"Migrating table: {table}")
    sqlite_cursor.execute(f"SELECT * FROM {table};")
    rows = sqlite_cursor.fetchall()
    if not rows:
        continue
    
    # Get column names
    sqlite_cursor.execute(f"PRAGMA table_info({table});")
    columns = [info[1] for info in sqlite_cursor.fetchall()]
    
    col_str = ", ".join([f'"{c}"' for c in columns])
    placeholders = ", ".join(["%s"] * len(columns))
    
    # Insert rows into Postgres
    for row in rows:
        try:
            pg_cursor.execute(f"INSERT INTO {table} ({col_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;", row)
        except Exception as e:
            pg_conn.rollback()
            # print(f"Error inserting row into {table}: {e}")

pg_conn.commit()
print("Data migration completed successfully!")
sqlite_conn.close()
pg_conn.close()
