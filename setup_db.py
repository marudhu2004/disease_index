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

c.execute('''CREATE TABLE IF NOT EXISTS causes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_id INTEGER,
                cause TEXT,
                FOREIGN KEY (disease_id) REFERENCES disease (id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_id INTEGER,
                symptom TEXT,
                FOREIGN KEY (disease_id) REFERENCES disease (id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS prevention (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_id INTEGER,
                prevention TEXT,
                FOREIGN KEY (disease_id) REFERENCES disease (id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS cure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_id INTEGER,
                cure TEXT,
                FOREIGN KEY (disease_id) REFERENCES disease (id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS specialists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_id INTEGER,
                specialist TEXT,
                FOREIGN KEY (disease_id) REFERENCES disease (id)
            )''')

conn.commit()
conn.close()
