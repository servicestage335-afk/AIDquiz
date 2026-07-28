import sqlite3
import os

db_path = 'db.sqlite3'
print(f"Checking database at: {os.path.abspath(db_path)}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", tables)

    cursor.execute("SELECT * FROM quiz_engine_subject")
    subjects = cursor.fetchall()
    print("Subjects in database:", subjects)

    cursor.execute("SELECT * FROM quiz_engine_quiz")
    quizzes = cursor.fetchall()
    print("Quizzes in database:", quizzes)

finally:
    conn.close()
