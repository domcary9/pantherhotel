# pantherhotel.py

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Function to create SQLite database table
def create_table():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            room_type TEXT,
            check_in_date TEXT,
            check_out_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_reservation(name, room_type, check_in_date, check_out_date):
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reservations (name, room_type, check_in_date, check_out_date) VALUES (?, ?, ?, ?)
    ''', (name, room_type, check_in_date, check_out_date))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

@app.route('/addrec', methods=['POST'])
def addrec():
    if request.method == 'POST':
        name = request.form['name']
        room_type = request.form['room_type']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        insert_reservation(name, room_type, check_in_date, check_out_date)
        return render_template('result.html', msg='Record successfully added')

@app.route('/reservation-list/')
def reservation_list():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservations')
    rows = cursor.fetchall()
    conn.close()
    return render_template('reservation-list.html', rows=rows)

if __name__ == '__main__':
    create_table()  # Create the database table if it doesn't exist
    app.run(debug=True)
