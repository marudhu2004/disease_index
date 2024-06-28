# setup_db.py
import sqlite3

conn = sqlite3.connect('diseases.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS disease (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS disease_info (
                disease_id INTEGER,
                causes TEXT,
                symptoms TEXT,
                prevention TEXT,
                cure TEXT,
                specialists TEXT,
                FOREIGN KEY (disease_id) REFERENCES disease (id)
            )''')

conn.commit()
conn.close()
