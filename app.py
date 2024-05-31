from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('database.db')

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tours (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    price REAL NOT NULL
                    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tours")
    tours = cur.fetchall()
    conn.close()
    return render_template('index.html', tours=tours)

# Сторінка додавання нового туру
@app.route('/add_tour', methods=['GET', 'POST'])
def add_tour():
    if request.method == 'POST':
        tour_data = request.form
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO tours (name, destination, price) VALUES (?, ?, ?)",
                    (tour_data['name'], tour_data['destination'], tour_data['price']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_tour.html')

if __name__ == '__main__':
    app.run(debug=True)