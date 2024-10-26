import sqlite3


# Function to initialize the database
def get_connection():
    conn = sqlite3.connect('student_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        roll_number INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        marks REAL NOT NULL
    )
    ''')
    conn.commit()
    return conn, cursor
