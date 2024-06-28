# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('diseases.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    diseases = conn.execute('SELECT * FROM disease').fetchall()
    conn.close()
    return render_template('index.html', diseases=diseases)

@app.route('/disease/<int:disease_id>')
def disease(disease_id):
    conn = get_db_connection()
    disease = conn.execute('SELECT * FROM disease WHERE id = ?', (disease_id,)).fetchone()
    info = conn.execute('SELECT * FROM disease_info WHERE disease_id = ?', (disease_id,)).fetchone()
    conn.close()
    return render_template('disease.html', disease=disease, info=info)

@app.route('/add_disease', methods=('GET', 'POST'))
def add_disease():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']

        conn = get_db_connection()
        conn.execute('INSERT INTO disease (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_disease.html')

@app.route('/add_info/<int:disease_id>', methods=('GET', 'POST'))
def add_info(disease_id):
    conn = get_db_connection()
    disease = conn.execute('SELECT * FROM disease WHERE id = ?', (disease_id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        causes = request.form['causes']
        symptoms = request.form['symptoms']
        prevention = request.form['prevention']
        cure = request.form['cure']
        specialists = request.form['specialists']

        conn = get_db_connection()
        conn.execute('INSERT INTO disease_info (disease_id, causes, symptoms, prevention, cure, specialists) VALUES (?, ?, ?, ?, ?, ?)', 
                     (disease_id, causes, symptoms, prevention, cure, specialists))
        conn.commit()
        conn.close()
        return redirect(url_for('disease', disease_id=disease_id))

    return render_template('add_info.html', disease_id=disease_id, disease=disease)


if __name__ == '__main__':
    app.run(debug=True)
