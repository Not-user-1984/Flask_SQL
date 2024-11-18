from flask import Flask, jsonify, request
import psycopg2
import json
from utility import measure_time

app = Flask(__name__)

# Параметры подключения к базе данных
DB_HOST = 'localhost'
DB_NAME = 'demo'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'


def get_db_connection():
    """Функция для установления соединения с базой данных."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )


@app.route('/bookings', methods=['GET'])
@measure_time
def get_bookings():
    """Получение всех бронирований."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM bookings;')
            bookings = cur.fetchall()
    return jsonify(bookings)


@app.route('/bookings/<book_ref>', methods=['GET'])
@measure_time
def get_booking(book_ref):
    """Получение бронирования по book_ref."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM bookings WHERE book_ref = %s;', (book_ref,))
            booking = cur.fetchone()
    return jsonify(booking) if booking else jsonify({'message': 'Booking not found'}), 404


@app.route('/bookings', methods=['POST'])
@measure_time
def create_booking():
    """Создание нового бронирования."""
    data = request.json
    book_ref = data.get('book_ref')
    book_date = data.get('book_date')
    total_amount = data.get('total_amount')

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO bookings (book_ref, book_date, total_amount) VALUES (%s, %s, %s) RETURNING *;',
                (book_ref, book_date, total_amount)
            )
            booking = cur.fetchone()
            conn.commit()
    return jsonify(booking), 201


@app.route('/bookings/<book_ref>', methods=['PUT'])
@measure_time
def update_booking(book_ref):
    """Обновление бронирования по book_ref."""
    data = request.json
    book_date = data.get('book_date')
    total_amount = data.get('total_amount')

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE bookings SET book_date = %s, total_amount = %s WHERE book_ref = %s RETURNING *;',
                (book_date, total_amount, book_ref)
            )
            booking = cur.fetchone()
            conn.commit()
    return jsonify(booking) if booking else jsonify({'message': 'Booking not found'}), 404


@app.route('/bookings/<book_ref>', methods=['DELETE'])
@measure_time
def delete_booking(book_ref):
    """Удаление бронирования по book_ref."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM bookings WHERE book_ref = %s RETURNING *;', (book_ref,))
            booking = cur.fetchone()
            conn.commit()
    return jsonify(booking) if booking else jsonify({'message': 'Booking not found'}), 404


@app.route('/aircrafts', methods=['POST'])
@measure_time
def add_aircraft():
    data = request.json
    aircraft_code = data['aircraft_code']
    model = json.dumps(data['model'])
    range = data['range']

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO aircrafts_data (aircraft_code, model, range) VALUES (%s, %s, %s)",
                (aircraft_code, model, range)
            )
            conn.commit()

    return jsonify({"message": "Aircraft added successfully"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
