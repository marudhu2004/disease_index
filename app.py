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
    causes = conn.execute('SELECT * FROM causes WHERE disease_id = ?', (disease_id,)).fetchall()
    symptoms = conn.execute('SELECT * FROM symptoms WHERE disease_id = ?', (disease_id,)).fetchall()
    prevention = conn.execute('SELECT * FROM prevention WHERE disease_id = ?', (disease_id,)).fetchall()
    cure = conn.execute('SELECT * FROM cure WHERE disease_id = ?', (disease_id,)).fetchall()
    specialists = conn.execute('SELECT * FROM specialists WHERE disease_id = ?', (disease_id,)).fetchall()
    conn.close()
    return render_template('disease.html', disease=disease, causes=causes, symptoms=symptoms, prevention=prevention, cure=cure, specialists=specialists)

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
    if request.method == 'POST':
        causes = request.form.getlist('causes')
        symptoms = request.form.getlist('symptoms')
        prevention = request.form.getlist('prevention')
        cure = request.form.getlist('cure')
        specialists = request.form.getlist('specialists')

        conn = get_db_connection()
        for cause in causes:
            conn.execute('INSERT INTO causes (disease_id, cause) VALUES (?, ?)', (disease_id, cause))
        for symptom in symptoms:
            conn.execute('INSERT INTO symptoms (disease_id, symptom) VALUES (?, ?)', (disease_id, symptom))
        for prevent in prevention:
            conn.execute('INSERT INTO prevention (disease_id, prevention) VALUES (?, ?)', (disease_id, prevent))
        for c in cure:
            conn.execute('INSERT INTO cure (disease_id, cure) VALUES (?, ?)', (disease_id, c))
        for specialist in specialists:
            conn.execute('INSERT INTO specialists (disease_id, specialist) VALUES (?, ?)', (disease_id, specialist))
        conn.commit()
        conn.close()
        return redirect(url_for('disease', disease_id=disease_id))

    return render_template('add_info.html', disease_id=disease_id)

if __name__ == '__main__':
    app.run(debug=True)
